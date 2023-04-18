import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.io.FileWriter;

import static java.lang.Math.sqrt;

public class AStar {
    private int hops;
    private double totalDistance;
    private City start;
    private City goal;
    private Boolean stdOut;
    private String fileName = null;
    private ArrayList<City> openNodes = new ArrayList<>();

    private ArrayList<City> path = new ArrayList<>();
    private ArrayList<City> visited = new ArrayList<>();
    public AStar(City start, City goal,Boolean stdOut,String fileName){
        this.hops = 0;
        this.totalDistance = 0;
        this.start = start;
        this.goal = goal;
        this.stdOut = stdOut;
        this.fileName = fileName;

    }
    /**
     * The main search algorithm.
     * Finds the path to the destination
     * Then calls the print functions
     * @throws IOException
     */
    public void AStarSearch() throws IOException {
        openNodes.add(start);
        start.setCostSoFar(0);
        start.setCostToGo(Distance(start,goal));
        start.setTotalCost(start.getCostSoFar() + start.getCostToGo());

        while (openNodes.size() > 0){
            City current = openNodes.remove(0);
            visited.add(visited.size(),current);
            if(current == goal){
                path.add(current);
                path(current);
                if(stdOut){
                    //print to stdOut
                    printStdOut();
                }
                else{
                    //print to output file
                    printFile();
                }
            }else{
                for (int i = 0; i<current.edges.size(); i++ ) {
                    City child = current.edges.get(i);
                    if (!isVisited(child) && !inOpenNodes(child)) {
                        double edgeDistance = Distance(current, child);
                        child.setCostSoFar(current.getCostSoFar() + edgeDistance);
                        child.setCostToGo(Distance(child,goal));
                        child.setTotalCost(child.getCostSoFar() + child.getCostToGo());
                        child.parent = current;
                        openNodes.add(openNodes.size(), child);
                    }
                }
                sort();
            }
        }
    }

    /**
     * Sorts the current openNodes to put the smallest total cost in the front of the open nodes
     */
    private void sort(){
        for(int i = 1; i< openNodes.size(); i++){
            int j = i;
            while(j>0){
                if(openNodes.get(j-1).getTotalCost() > openNodes.get(j).getTotalCost()){
                    City temp = openNodes.get(j-1);
                    openNodes.set(j-1,openNodes.get(j));
                    openNodes.set(j,temp);
                }
                j--;
            }


        }

    }
    /**
     * Checks to see if the current city is visited
     * @param city the current city
     * @return true if the city has already been visited
     */
    private boolean isVisited(City city){
        for(City c : visited){
            if(city == c){
                return true;
            }
        }
        return false;
    }

    /**
     * Checks to see if the currently city is already open
     * @param city the current city
     * @return true if the city is open
     */
    private boolean inOpenNodes(City city)
    {
        for(City c: openNodes){
            if(city == c){
                return true;
            }
        }
        return false;
    }
    /**
     * Creates the solution path based on the initial search
     * @param city the current city
     * @return the arrayList of the path to the solution
     */
    private ArrayList<City> path(City city){
        if(city == start){
            hops = path.size() - 1;
            return path;
        }else{
            City c = city.parent;
            path.add(0,c);
            double distance = Distance(city, c);
            totalDistance+=distance;
            return path(c);
        }
    }

    /**
     * Calcualtes the edge distance between two cities using longitude and latitude
     * @param city1 the start city
     * @param city2 the end city
     * @return a double of the distance between the cities
     */
    private double Distance(City city1, City city2){
        return sqrt(Math.pow((city1.getLatitude()-city2.getLatitude()),2) + Math.pow((city1.getLongitude() - city2.getLongitude()),2)) * 100;
    }
    /**
     * Print statement for standard out
     */
    private void printStdOut(){
        System.out.println("A* Search Results: ");
        for(City city: path){
            System.out.println(city.getCityName());
        }
        System.out.println("That took " + hops +  " hops to find.");
        System.out.println("Total distance = " + Math.round(totalDistance) + " miles.\n\n");
    }
    /**
     * Print Statement for file output
     * @throws IOException
     */
    private void printFile() throws IOException {
        BufferedWriter out = new BufferedWriter(new FileWriter(fileName + ".txt", true));
        out.write("A* Search Results: \n");
        for (City city : path) {
            out.write(city.getCityName() + "\n");
        }
        out.write("That took " + hops + " hops to find.\n");
        out.write("Total distance = " + Math.round(totalDistance) + " miles.\n\n");
        out.close();
    }
}