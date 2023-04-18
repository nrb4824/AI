import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.io.FileWriter;

import static java.lang.Math.sqrt;

public class DFS {
    private int hops;
    private double totalDistance;
    private City start;
    private City goal;
    private Boolean stdOut;
    private String fileName = null;
    private ArrayList<City> stack = new ArrayList<>();

    private ArrayList<City> path = new ArrayList<>();
    private ArrayList<City> visited = new ArrayList<>();

    public DFS(City start, City goal, Boolean stdOut, String fileName) {
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
    public void DFSSearch() throws IOException {
        stack.add(start);
        while (stack.size() > 0) {
            City current = stack.remove(0);
            visited.add(visited.size(), current);
            if (current == goal) {
                path.add(current);
                path(current);
                if (stdOut) {
                    //print to stdOut
                    printStdOut();
                } else {
                    //print to output file
                    printFile();
                }
            } else {
                sort(current);
                //for loop in reverse so that cities enter the stack in the correct order
                for (int i = 0; i < current.edges.size(); i++ ) {
                    City child = current.edges.get(i);
                    if (!isVisited(child) && !inStack(child)) {
                        child.parent = current;
                        stack.add(0, child);
                    }
                }
            }
        }
    }

    /**
     * Sorts the edges of the cities so that they are in alphabetical order
     * @param city The city to sort edges
     */
    private void sort(City city) {
        for (int i = 1; i < city.edges.size(); i++) {
                int j = i;
                while(j>0){
                    if (city.edges.get(j-1).getCityName().compareToIgnoreCase(city.edges.get(j).getCityName()) < 0) {
                        City temp = city.edges.get(j-1);
                        city.edges.set(j-1, city.edges.get(j));
                        city.edges.set(j, temp);
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
    private boolean isVisited(City city) {
        for (City c : visited) {
            if (city == c) {
                return true;
            }
        }
        return false;
    }

    /**
     * Checks to see if the currenty city is already in the stack
     * @param city the current city
     * @return true if the city is in the stack
     */
    private boolean inStack(City city) {
        for (City c : stack) {
            if (city == c) {
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
    private ArrayList<City> path(City city) {
        if (city == start) {
            hops = path.size() - 1;
            return path;
        } else {
            City c = city.parent;
            path.add(0, c);
            double distance = sqrt(Math.pow((city.getLatitude() - c.getLatitude()), 2) + Math.pow((city.getLongitude() - c.getLongitude()), 2)) * 100;
            totalDistance += distance;
            return path(c);
        }
    }

    /**
     * Print statement for standard out
     */
    public void printStdOut() {
        System.out.println("Depth-First Search Results: ");
        for (City city : path) {
            System.out.println(city.getCityName());
        }
        System.out.println("That took " + hops + " hops to find.");
        System.out.println("Total distance = " + Math.round(totalDistance) + " miles.\n\n\n");
    }

    /**
     * Print Statement for file output
     * @throws IOException
     */
    public void printFile() throws IOException {
        BufferedWriter out = new BufferedWriter(new FileWriter(fileName + ".txt", true));
        out.write("Depth-First Search Results: \n");
        for (City city : path) {
            out.write(city.getCityName() + "\n");
        }
        out.write("That took " + hops + " hops to find.\n");
        out.write("Total distance = " + Math.round(totalDistance) + " miles.\n\n\n");
        out.close();
    }
}
