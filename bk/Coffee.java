
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;
import com.google.gson.Gson;

class Ingredient {

    private final String name;
    private final BigDecimal cost;
}

class Recipe {

    private final String name;
    private final List<Ingredient> ingredients = new ArrayList<>();
}

class Coffee {

    public static void main(String args[]) {
        JsonReader in = new JsonReader(new FileReader("kk.txt"));
        while (in.hasNext()) {
            String fieldName = in.nextString();

            if (in.peek() == JsonToken.NULL) {
                in.nextNull();
                continue;
            }

            switch (fieldName) {
                case "machine": {
                    type = in.nextString();
                    break;
                }
                case "BODY": {
                    body = JsonParser.parseReader(in);
                    break;
                }
                default: {
                    in.skipValue();
                }
            }
        }
    }
}
