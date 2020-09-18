package eu.qanswer.data2rdf.mappings.imageannotation;

import eu.qanswer.data2rdf.configuration.CSVConfigurationFile;
import eu.qanswer.data2rdf.configuration.CustomMapping;
import eu.qanswer.data2rdf.configuration.Mapping;
import eu.qanswer.data2rdf.configuration.Type;
import eu.qanswer.data2rdf.utility.Utility;
import org.apache.jena.graph.Node;
import org.apache.jena.graph.NodeFactory;
import org.apache.jena.graph.Triple;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

public class ObjectPosition extends CSVConfigurationFile {
    private String qanswerEndPoint = "https://qanswer-core1.univ-st-etienne.fr/";
    private HashMap<String, String> labelQuery = new HashMap<>();
    private HashSet<String> labelAndWdImgAdded = new HashSet<>();

    public ObjectPosition() {
        this("/home/diazork/FAC/M1/stage/stage/data2rdf/src/main/resources/imageHasOnLeftRightCenterTopBottom.csv");
    }

    public ObjectPosition(String filepath) {
        format = "csv";
        separator = ',';
        file = filepath;
        baseUrl = "http://qanswer.eu/data/datasets/objectPosition/";
        //key = "Image name";
        key = "mpageid";
        mappings = new ArrayList<>(Arrays.asList(
                new Mapping("has on the left", baseUrl + "has_on_the_left", new Linking(), Type.CUSTOM),
                new Mapping("has on the right", baseUrl + "has_on_the_right", new Linking(), Type.CUSTOM),
                new Mapping("has on the top", baseUrl + "has_on_the_top", new Linking(), Type.CUSTOM),
                new Mapping("has on the bottom", baseUrl + "has_on_the_bottom", new Linking(), Type.CUSTOM),
                new Mapping("has in the center", baseUrl + "has_in_the_center", new Linking(), Type.CUSTOM)
        ));
        triples = new ArrayList<>(Arrays.asList(
                // English
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_left"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has on the left", "en")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_right"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has on the right", "en")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_top"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has on the top", "en")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_bottom"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has on the bottom", "en")),
                new Triple(NodeFactory.createURI(baseUrl + "has_in_the_center"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has in the center", "en")),
                new Triple(NodeFactory.createURI(baseUrl + "has_in_the_center"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("has in the middle", "en")),
                // French
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_left"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a sur la gauche", "fr")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_right"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a sur la droite", "fr")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_top"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a sur le dessus", "fr")),
                new Triple(NodeFactory.createURI(baseUrl + "has_on_the_bottom"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a sur le dessous", "fr")),
                new Triple(NodeFactory.createURI(baseUrl + "has_in_the_center"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a au centre", "fr")),
                new Triple(NodeFactory.createURI(baseUrl + "has_in_the_center"),
                        NodeFactory.createURI("http://www.w3.org/2000/01/rdf-schema#label"),
                        NodeFactory.createLiteral("a au milieu", "fr"))
        ));
    }

    private class Linking extends CustomMapping {

        @Override
        public ArrayList<Triple> function(Node subject, HashMap<String, String> article) {
            Utility utility = new Utility();
            ArrayList<Triple> triples = new ArrayList<>();

            Node object = null;
            //System.out.println(article);
            for (String a : article.keySet()) {
                subject = utility.createURI(article.get("mpageid"));
                if (a.contains("Image name")) {
                    if (!labelAndWdImgAdded.contains(subject.toString())) {
                        labelAndWdImgAdded.add(subject.toString());
                        triples.add(
                                new Triple(
                                        subject,
                                        utility.createURI("http://www.wikidata.org/prop/direct/P31"),
                                        utility.createURI("http://www.wikidata.org/entity/Q478798")
                                )
                        );
                    }
                } else if (a.contains(getMapping().getTag())) {
                    if (!article.get(getMapping().getTag()).equals("na") & !article.get(getMapping().getTag()).equals("")) {
                        //subject = utility.createURI(article.get("mpageid"));
                        object = utility.createURI(article.get(getMapping().getTag()));
                        Node predicate = utility.createURI(getMapping().getPropertyUri());
                        triples.add(new Triple(subject, predicate, object));
                        /*
                        System.out.println(article.get("object name"));
                        System.out.println(subject);
                        System.out.println(predicate);
                        System.out.println(object);
                        System.out.println("=====");
                        //*/
                    }
                }
            }
            return triples;
        }
    }
}
