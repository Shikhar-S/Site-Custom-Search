import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.update.UpdateRequest;
import org.elasticsearch.action.update.UpdateResponse;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentFactory;
import org.elasticsearch.rest.RestStatus;
import org.elasticsearch.transport.client.PreBuiltTransportClient;

import java.net.InetAddress;

import static org.elasticsearch.common.xcontent.XContentFactory.jsonBuilder;

public class Indexer {
    Settings settings=null;
    TransportClient client=null;
    public Indexer()
    {
        try{
            settings = Settings.builder()
                    .put("cluster.name", "elasticsearch").build();
            client = new PreBuiltTransportClient(settings)
                    .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("localhost"), 9300));

        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

    }
    public String indexDocument(String title,String baseURL,String URL,String body,String headings,String crawlerName,String id)throws Exception
    {
        IndexResponse elasticSearchresponse;
        XContentBuilder builder;
        if(id.equals("New"))
        {
             builder = jsonBuilder()
                    .startObject()
                    .field("title", title)
                    .field("baseURL",baseURL)
                    .field("url", URL)
                    .field("content", body)
                    .field("heading",headings)
                    .endObject();
            elasticSearchresponse = client.prepareIndex("articles",crawlerName)
                    .setSource(builder).get();

            return (elasticSearchresponse.getId());

        }
        else
        {
            IndexRequest indexRequest = new IndexRequest("articles", crawlerName, id)
                    .source(jsonBuilder()
                            .startObject()
                            .field("title", title)
                            .field("baseURL",baseURL)
                            .field("url", URL)
                            .field("content", body)
                            .field("heading",headings)
                            .endObject());
            UpdateRequest updateRequest = new UpdateRequest("articles", crawlerName, id)
                    .doc(jsonBuilder()
                            .startObject()
                            .field("title", title)
                            .field("baseURL",baseURL)
                            .field("url", URL)
                            .field("content", body)
                            .field("heading",headings)
                            .endObject())
                    .upsert(indexRequest);
            UpdateResponse updateResponse = client.update(updateRequest).get();
            return updateResponse.getId();
        }
    }
}
