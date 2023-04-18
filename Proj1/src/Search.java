
import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class Search {
    /**
     * Reads in file edge.dat and city.dat and creates a node tree.
     * Takes in user input, if the user inputed a file it reads the file
     * Can either output to standard output or a file of the specified name
     * Use a "-" for standard input/output and enter the name of the file otherwise
     * @param args The passed in arguments
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
        String startCityName = null;
        String goalCityName = null;
        City startCity = null;
        City goalCity = null;
        boolean stdOut = false;
        ArrayList<City> cities = new ArrayList<>();
        String outputFileName = null;
        City city1 = null;
        City city2 = null;

        if(args.length != 2){
            System.err.println("Usage: java Search inputFile outputFile");
            System.exit(0);
        }

        // Reads the input file
        if(!args[0].equals("-")){
            try{
                Scanner inputFile = new Scanner(new File(args[0]));
                while(inputFile.hasNext()){
                    startCityName = inputFile.next();
                    goalCityName = inputFile.next();
                }
                inputFile.close();
            }catch(Exception E){
                System.err.println("File not found: " + args[0]);
                System.exit(0);
            }
        }else{
            Scanner inputScanner = new Scanner(System.in);
            System.out.println("Enter the start city");
            startCityName = inputScanner.nextLine();
            System.out.println("Enter the destination");
            goalCityName = inputScanner.nextLine();
        }

        if(args[1].equals("-")){
            stdOut = true;
        }
        else{
            outputFileName = args[1];
        }

        //reads in the city.dat file and generates a list of cities with, names, states, latitudes, and longitudes
        try{
            Scanner cityFile = new Scanner(new File("city.dat"));
            while (cityFile.hasNext()) {
                City city = new City(cityFile.next(),cityFile.next(),cityFile.nextFloat(),cityFile.nextFloat());
                cities.add(city);
            }
            cityFile.close();
        }catch(Exception E){
            System.err.println("File not found: city.dat");
            System.exit(0);
        }


        //reads in the edge.dat file and adds each edge to the list of connecting cities for each city
        try{

            Scanner edgeFile = new Scanner(new File("edge.dat"));
            while(edgeFile.hasNext()) {
                String cityName1 = edgeFile.next();
                String cityName2 = edgeFile.next();
                for(City city: cities){
                    if(city.getCityName().equals(cityName1)){
                        city1 = city;
                    }
                    else if(city.getCityName().equals(cityName2)){
                        city2 = city;
                    }
                }
                for(City city:cities){
                    if(city.getCityName().equals(cityName1)){
                        city.addEdge(city2);
                    }
                    else if(city.getCityName().equals(cityName2)){
                        city.addEdge(city1);
                    }
                }
            }
            edgeFile.close();
        }catch(Exception E){
            System.err.println("File not found: edge.dat");
            System.exit(0);
        }

        //checks to see if the cities read in are actual cities, if not throws error
        for(City city: cities){
            if(startCityName.equals(city.getCityName())){
                startCity = city;
            }
            else if(goalCityName.equals(city.getCityName())){
                goalCity = city;
            }
        }
        if(startCity == null){
            System.err.println("No such city: " + startCityName);
            System.exit(0);
        }
        else if(goalCity == null){
            System.err.println("No such city: " + goalCityName);
            System.exit(0);
        }

        // Calls the 3 Search algorithms
        BFS bfs = new BFS(startCity, goalCity, stdOut, outputFileName);
        bfs.BFSSearch();

        DFS dfs = new DFS(startCity,goalCity,stdOut, outputFileName);
        dfs.DFSSearch();

        AStar A = new AStar(startCity, goalCity, stdOut, outputFileName);
        A.AStarSearch();
    }
}