import net.media.mnetcrawler.*;
import net.media.mnetcrawler.bean.SyncCrawlResponse;
import net.media.mnetcrawler.util.RotatingUserAgentManager;
import net.media.mnetcrawler.util.UserAgentManager;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

import java.sql.*;
import java.util.*;

public class MultiCrawler {
    public static void main(String args[])throws Exception
    {

        boolean makeNewDatabase=true;
        Connection sqlConnection=null;
        try{
            sqlConnection=DriverManager.getConnection("jdbc:sqlite:sample.db");
            Statement statement = sqlConnection.createStatement();
            statement.setQueryTimeout(30);  // set timeout to 30 sec.


            //comment 3 lines for not creating a new table on every iter.
            if(makeNewDatabase)
            {
                statement.executeUpdate("drop table if exists crawled_urls");
                statement.executeUpdate("create table crawled_urls (url string,hash string,baseURL string,crawlerName string,elasticID string,creation_time integer)");
                System.out.println("Created table for URLs");
            }

            IndexUpdater updater=new IndexUpdater();
            updater.start();
            System.out.println("Started updater");

            Jedis jedisSubscriber=new Jedis();
            System.out.println("Started Redis server");
            System.out.println("Waiting for URLs");



            jedisSubscriber.subscribe(new QueueListener(),"messagequeue");



        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
        finally {
            try{
                if(sqlConnection!=null)
                    sqlConnection.close();
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
        }


        /*

        try
        {
            // create a database connection

            Statement statement = connection.createStatement();
            statement.setQueryTimeout(30);  // set timeout to 30 sec.

            statement.executeUpdate("drop table if exists crawled_urls");
            statement.executeUpdate("create table crawled_urls (url string)");
            statement.executeUpdate("insert into crawled_urls values('leo')");
            ResultSet rs = statement.executeQuery("select * from crawled_urls where url='leo'");
            while(rs.next())
            {
                // read the result set
                System.out.println("name = " + rs.getString("url"));
            }
        }
        catch(SQLException e)
        {
            // if the error message is "out of memory",
            // it probably means no database file is found
            System.err.println(e.getMessage());
        }
        finally
        {
            try
            {
                if(connection != null)
                    connection.close();
            }
            catch(SQLException e)
            {
                // connection close failed.
                System.err.println(e);
            }
        }


        */

        /*String url="https://www.thehindu.com";
        try{
            UserAgentManager userAgentManager = new RotatingUserAgentManager();
            CrawlerConfig crawlerConfig=new DefaultProxyCrawlerConfig("Crawler",userAgentManager);
            crawl(url,crawlerConfig);
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }*/
    }



}
