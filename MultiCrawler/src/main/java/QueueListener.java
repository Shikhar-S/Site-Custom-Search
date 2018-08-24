import redis.clients.jedis.JedisPubSub;

import java.sql.Connection;

public class QueueListener extends JedisPubSub {

    @Override
    public void onMessage(String channel, String message) {
        try {
            Crawler c = new Crawler(message);
            c.start();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

}
