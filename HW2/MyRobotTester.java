import world.World;

public class MyRobotTester {

    public static void main(String[] args) {
        try {
            World myWorld = new World("TestCases/myInputFile6.txt", false);

            RobotTraveler robot = new RobotTraveler();
            robot.addToWorld(myWorld);
            myWorld.createGUI(400, 400, 200); // uncomment this and create a GUI; the last parameter is delay in msecs


            robot.travelToDestination();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
