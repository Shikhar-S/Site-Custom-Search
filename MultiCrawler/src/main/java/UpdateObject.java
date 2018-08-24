import java.sql.ResultSet;

public class UpdateObject {
    String URL, hashold, baseURL, crawlerName, ESid;
    long time;
    public UpdateObject(ResultSet rs)
    {
        try{
            URL= rs.getString("url");
            hashold=rs.getString("hash");
            baseURL=rs.getString("baseURL");
            crawlerName=rs.getString("crawlerName");
            ESid=rs.getString("elasticID");
            time=rs.getInt("creation_time");
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }


    }
}
