import java.util.ArrayList;

public class City {
    private String cityName;
    private String state;
    private float latitude;
    private float longitude;
    public ArrayList<City> edges;

    public City parent;



    private double costSoFar;
    private double costToGo;
    private double totalCost;

    public City(String cityName, String state, float latitude, float longitude) {
        this.cityName = cityName;
        this.state = state;
        this.latitude = latitude;
        this.longitude = longitude;
        this.edges = new ArrayList<>();
    }

    public String getCityName() {
        return cityName;
    }

    public void setCityName(String cityName) {
        this.cityName = cityName;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public float getLatitude() {
        return latitude;
    }

    public void setLatitude(float latitude) {
        this.latitude = latitude;
    }

    public float getLongitude() {
        return longitude;
    }

    public void setLongitude(float longitude) {
        this.longitude = longitude;
    }

    public void addEdge(City city) {
        edges.add(city);
    }

    public double getCostSoFar() {return costSoFar;}

    public void setCostSoFar(double costSoFar) {this.costSoFar = costSoFar;}

    public double getCostToGo() {return costToGo;}

    public void setCostToGo(double costToGo) {this.costToGo = costToGo;}

    public double getTotalCost() {return totalCost;}

    public void setTotalCost(double totalCost) {this.totalCost = totalCost;}
}
