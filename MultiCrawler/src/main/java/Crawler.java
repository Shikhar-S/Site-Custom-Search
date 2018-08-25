import net.media.mnetcrawler.CrawlerConfig;
import net.media.mnetcrawler.DefaultProxyCrawlerConfig;
import net.media.mnetcrawler.SyncCrawler;
import net.media.mnetcrawler.bean.SyncCrawlResponse;
import net.media.mnetcrawler.util.RotatingUserAgentManager;
import net.media.mnetcrawler.util.UserAgentManager;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import redis.clients.jedis.Jedis;

import java.math.BigInteger;
import java.net.InetAddress;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Calendar;

public class Crawler extends Thread {
    public String crawlURL;
    public String crawlerName;
    Connection SqlConnection = null;
    UserAgentManager userAgentManager=null;
    CrawlerConfig crawlerConfig=null;
    final int MAX_DEPTH=4;
    final int MAX_BREADTH=15;
    public Crawler(String message)
    {
        int splitAt=message.indexOf(' ');
        this.crawlerName=message.substring(0,splitAt);
        this.crawlURL=message.substring(splitAt+1);
        try{
            this.userAgentManager = new RotatingUserAgentManager();
            this.crawlerConfig=new DefaultProxyCrawlerConfig("Crawler",userAgentManager);
            //Class.forName("org.sqlite.JDBC");
            this.SqlConnection= DriverManager.getConnection("jdbc:sqlite:sample.db");
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
    public void run()
    {
        System.out.println("Starting crawling on: "+crawlURL);
        try {
            crawl(true,true,1000);
            this.SqlConnection.close();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
    public void crawl(boolean save,boolean restore,int saveAt)throws Exception
    {
        //check for repetition in crawlername, domainURL : both should be unique
        Queue<Pair> Q=new LinkedList<Pair>();
        int iter=0;
        if(restore)
        {
            try {
                Jedis jedis = new Jedis();
                String value;
                while (true) {
                    try {
                        value = jedis.lpop(crawlerName);
                        if (value == null) { //end of redis frontier
                            break;
                        }
                        int sp_idx = value.indexOf(' ');
                        int depth = Integer.parseInt(value.substring(0, sp_idx));
                        String url = value.substring(sp_idx + 1);
                        Q.add(new Pair(url, depth));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
                if(!Q.isEmpty())
                    System.out.println("Loaded from saved state");
            }
            catch (Exception e)
            {
                e.printStackTrace();
                Q.add(new Pair(crawlURL,0)); //if jedis restoration fails crawl again
            }
        }
        else
        {
            Q.add(new Pair(crawlURL,0));
        }


        String baseURL=crawlURL;
        HashMap<String, Boolean> set=new HashMap<String, Boolean>();
        if(Q.isEmpty())
        {
            Q.add(new Pair(baseURL,0));
        }


        set.put(baseURL,true);


        MessageDigest m = MessageDigest.getInstance("MD5");



        Statement statement = SqlConnection.createStatement();
        statement.setQueryTimeout(30);  // set timeout to 30 sec.

        Indexer indexer=new Indexer();

        SyncCrawler syncCrawler = new SyncCrawler(crawlerConfig);

        while(!(Q.isEmpty()))
        {
            iter++;
            if(save && (iter%saveAt)==0)
            {
             try
             {
                 Jedis jedis=new Jedis();
                 jedis.del(crawlerName);
                 for(Pair p: Q)
                 {
                     jedis.rpush(crawlerName,p.depth+" "+p.url);
                 }
                 System.out.println("Saved frontier at iteration: "+iter);
             }
             catch (Exception e)
             {
                 e.printStackTrace();
             }
            }
            int breadth_counter=0;
            Pair x=Q.poll();
            String URL=x.url;
            int depth_counter=x.depth;
            if(depth_counter>MAX_DEPTH) //dont go further on this branch
                continue;

            SyncCrawlResponse response;
            try {
                response = syncCrawler.crawl(URL);
            }
            catch(Exception e)
            {
                continue;
            }

            ////////////////Extract fields//////////////
            String content=response.getContent();
            Document soup= Jsoup.parse(content);
            soup.setBaseUri(URL);
            Elements headings_e=soup.select("h1,h2,h3,h4,h5,h6");
            String headings="";
            for(Element heading : headings_e)
                headings+=(heading.text()+" ");

            String title=soup.select("title").text();
            String body=soup.body().text();
            ////////////////////////////////////////////

            ////////////////Generate hash///////////////
            String getHashof=title+body+headings;
            m.reset();
            m.update(getHashof.getBytes());
            byte[] digest = m.digest();
            BigInteger bigInt = new BigInteger(1,digest);
            String hashtext = bigInt.toString(16);
            ////////////////////////////////////////////

            //////////////Check if in SQL///////////////
            //doesnt worry about repeat entries in sql table. Worries about repeat entries in ES index.
            String searchQuery=String.format("select * from crawled_urls where url='%s' and hash='%s'",URL,hashtext);
            ResultSet rs = statement.executeQuery(searchQuery);
            boolean resultExists=rs.next();
            try {
                rs.close();
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
            if(resultExists) //dont add to index if values are same
            {
                System.out.println("Crawler: Already in database: "+URL+" hash:"+hashtext);
            }
            else{



                try {
                    ////////////////Add to ES here///////////////
                    String ESid=indexer.indexDocument(title,baseURL,URL,body,headings,crawlerName,"New");
                    System.out.println("Added : "+URL );
                    /////////////////Add to SQL//////////////////
                    long timeinMilli=Calendar.getInstance().getTimeInMillis();
                    String sqlQuery = String.format("insert into crawled_urls values('%s','%s','%s','%s','%s',%d)", URL, hashtext, baseURL, crawlerName, ESid,timeinMilli);
                    statement.executeUpdate(sqlQuery);
                    System.out.println("Added to SQL- hash: " + hashtext);
                }
                catch(Exception e) //already in database, got updated from updater
                {
                    e.printStackTrace();
                }
            }


            Elements links=soup.select("a[href]");
            //System.out.println(links.size());
            int added=0;
            for ( Element link : links)
            {
                if(breadth_counter>MAX_BREADTH)
                    break;
                String childURL=link.attr("abs:href");
                if(childURL.indexOf('#')>=0) //ignore pointer urls on same page
                    continue;

                if(childURL.startsWith(baseURL))
                {

                    if(set.get(childURL)==null)
                    {
                        breadth_counter++;
                        added++;
                        set.put(childURL,true);
                        Q.add(new Pair(childURL,depth_counter+1));

                    }

                }

            }
            //System.out.println("URLS added in this iteration: "+added);



        }
        System.out.println("Finished crawling on: "+baseURL);
        System.out.println("Q size-> "+Q.size());


    }
}
