import net.media.mnetcrawler.CrawlerConfig;
import net.media.mnetcrawler.DefaultProxyCrawlerConfig;
import net.media.mnetcrawler.SyncCrawler;
import net.media.mnetcrawler.bean.SyncCrawlResponse;
import net.media.mnetcrawler.util.RotatingUserAgentManager;
import net.media.mnetcrawler.util.UserAgentManager;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.sql.*;
import java.util.Calendar;

public class IndexUpdater extends Thread{
    long updatedTill;
    Connection SqlConnection = null;
    UserAgentManager userAgentManager=null;
    CrawlerConfig crawlerConfig=null;
    Indexer indexer=null;
    final int MAX_BREADTH_UPDATE=10;
    final int UPDATE_SET_SIZE=1;
    public IndexUpdater()
    {
        updatedTill=0;
        indexer=new Indexer();
        try{
            this.userAgentManager = new RotatingUserAgentManager();
            this.crawlerConfig=new DefaultProxyCrawlerConfig("Updater",userAgentManager);
            //Class.forName("org.sqlite.JDBC");
            this.SqlConnection= DriverManager.getConnection("jdbc:sqlite:sample.db");
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
    public void handleOldURL(Statement statement,MessageDigest m ,SyncCrawler syncCrawler,String URL,String baseURL,String crawlerName,String ESid) //insert in es with new key
    {
        SyncCrawlResponse response;
        try {
            response = syncCrawler.crawl(URL);
            ////////////////////Extract fields///////////////////
            String content=response.getContent();
            Document soup= Jsoup.parse(content);
            soup.setBaseUri(URL);

            Elements headings_e=soup.select("h1,h2,h3,h4,h5,h6");
            String headings="";
            for(Element heading : headings_e)
                headings+=(heading.text()+" ");

            String title=soup.select("title").text();
            String body=soup.body().text();
            //////////////////////////////////////////////
            ////////////////Generate hash////////////////
            String getHashof=title+body+headings;
            m.reset();
            m.update(getHashof.getBytes());
            byte[] digest = m.digest();
            BigInteger bigInt = new BigInteger(1,digest);
            String hashtext = bigInt.toString(16);
            /////////////////////////////////////////////

            try {
                indexer.indexDocument(title, baseURL, URL, body, headings, crawlerName, ESid);
                String updateEntry = String.format("update crawled_urls set hash='%s', creation_time=%d where url='%s'", hashtext, URL,Calendar.getInstance().getTimeInMillis());
                statement.executeUpdate(updateEntry);
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
            return;
        }

    }
    public void run()
    {
        Statement statement;
        while(true)
        {
            //checks for changes in hash and adds link to be handled in next cycle with hash 0 and also updates text changes in doc in es using esid.

            try
            {
                Thread.sleep(1000000000);
                MessageDigest m = MessageDigest.getInstance("MD5");
                statement = SqlConnection.createStatement();
                statement.setQueryTimeout(30);  // set timeout to 30 sec.
                String getQuery=String.format("select top %d * from crawled_urls where creation_time>%d",UPDATE_SET_SIZE,updatedTill);
                ResultSet rs = statement.executeQuery(getQuery);
                SyncCrawler syncCrawler = new SyncCrawler(crawlerConfig);
                int len=0;
                UpdateObject[] updateObjects=new UpdateObject[UPDATE_SET_SIZE];
                while(rs.next() && len<UPDATE_SET_SIZE)
                {
                    updateObjects[len]=new UpdateObject(rs);
                    len++;
                }
                rs.close();

                for(int i=0;i<UPDATE_SET_SIZE && i<len;i++)
                {

                    // read the result set

                    String URL= updateObjects[i].URL;
                    String hashold=updateObjects[i].hashold;
                    String baseURL=updateObjects[i].baseURL;
                    String crawlerName=updateObjects[i].crawlerName;
                    String ESid=updateObjects[i].ESid;
                    updatedTill=updateObjects[i].time;

                    if(hashold.equals("0")) //added during last update cycle.
                    {
                            handleOldURL(statement,m,syncCrawler,URL,baseURL,crawlerName,ESid);
                            continue;
                    }

                    SyncCrawlResponse response;
                    try {
                        response = syncCrawler.crawl(URL);
                    }
                    catch(Exception e)
                    {
                        continue;
                    }
                    ////////////////////Extract fields///////////////////
                    String content=response.getContent();
                    Document soup= Jsoup.parse(content);
                    soup.setBaseUri(URL);


                    Elements headings_e=soup.select("h1,h2,h3,h4,h5,h6");
                    String headings="";
                    for(Element heading : headings_e)
                        headings+=(heading.text()+" ");

                    String title=soup.select("title").text();
                    String body=soup.body().text();
                    //////////////////////////////////////////////

                    ////////////////Generate hash////////////////
                    String getHashof=title+body+headings;
                    m.reset();
                    m.update(getHashof.getBytes());
                    byte[] digest = m.digest();
                    BigInteger bigInt = new BigInteger(1,digest);
                    String hashtext = bigInt.toString(16);
                    /////////////////////////////////////////////

                    //////////////Check if in SQL///////////////

                    if(hashold.equals(hashtext)) //don't add to index if values are same
                    {
                        System.out.println("Already in database: "+URL+" hash:"+hashold);
                    }
                    else{
                        ////////////////Add to ES here///////////////
                        indexer.indexDocument(title,baseURL,URL,body,headings,crawlerName,ESid);

                        System.out.println("Added : "+URL );
                        ///////////////////////////////////////////
                        try {
                            /////////////////Add to SQL//////////////////
                            String sqlQuery = String.format("insert into crawled_urls values('%s','%s','%s','%s','%s')", URL, hashtext, baseURL, crawlerName, ESid);
                            statement.executeUpdate(sqlQuery);
                            System.out.println("Added to SQL- hash: " + hashtext);
                            /////////////////////////////////////////////
                        }
                        catch(Exception e)
                        {
                            e.printStackTrace();
                        }

                        ///iterate on child and add to sql with hash 0/////
                        Elements links=soup.select("a[href]");
                        int breadth_counter=0;

                        for ( Element link : links)
                        {


                            if(breadth_counter>MAX_BREADTH_UPDATE)
                                break;

                            String childURL=link.attr("abs:href");
                            if(childURL.startsWith(baseURL+"#")) //ignore pointer urls on same page
                                continue;
                            if(childURL.startsWith(baseURL))
                            {
                                String findQuery=String.format("select * from crawled_urls where url='%s'",childURL);
                                try{
                                    ResultSet childRs=statement.executeQuery(findQuery);
                                    if(!(childRs.next()))
                                    {
                                        breadth_counter++;
                                        String insertEmpty=String.format("insert into crawled_urls values('%s','%s','%s','%s','%s',%d)",childURL,"0",baseURL,crawlerName, "New", Calendar.getInstance().getTimeInMillis());
                                        statement.executeUpdate(insertEmpty);
                                    }
                                    childRs.close();
                                }
                                catch (Exception e)
                                {
                                    e.printStackTrace();
                                }


                            }
                        }


                    }
                }
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
        }


    }

}
