// Feel free to use this java file as a template and extend it to write your solver.
// ---------------------------------------------------------------------------------

import world.Robot;
import world.World;

import java.awt.*;
import java.util.*;
import java.util.List;

public class RobotTraveler extends Robot {

    private Point start;
    private Point destination;
    private int cols;
    private int rows;
    private Map<Point, Point> cameFrom;
    private List<Point> evaluated;
    private List<Point> notEvaluated;
    private List<Point> walls;
    private List<Point> nonWalls;
    Map<Point, Double> gScores;
    Map<Point, Double> fScores;
    boolean isUncertain;

    public RobotTraveler() {
        super();
    }

    @Override
    public void travelToDestination() {
        long startTime = System.nanoTime();
        List<Point> path = aStar(start, destination);
        long estimatedTime = System.nanoTime() - startTime;
        System.out.println("Time it took to generate path: " + Math.pow(10, -9) * estimatedTime + " s");
        if (!path.isEmpty()) {
            for (Point node : path) {
                super.move(node);
            }
        } else {
            System.out.println("You were either at the destination already or there wasn't a valid path to get there!");
        }
    }

    @Override
    public void addToWorld(World world) {
        isUncertain = world.getUncertain();
        start = world.getStartPos();
        destination = world.getEndPos();
        cols = world.numCols();
        rows = world.numRows();
        super.addToWorld(world);
    }

    // Modified Manhattan distance allowing for diagonal, where the cost of moving diagonally is slightly greater than moving straight, but is not Euclidean in cost,
    // not Chebyshev distance, or pure, unmodified Manhattan distance.
    // http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    public Double heuristic(Point p, Point d) {
        double dx = Math.abs(p.getX() - d.getX());
        double dy = Math.abs(p.getY() - d.getY());
        if (isUncertain && !walls.contains(d) && !nonWalls.contains(d)) {
            int numOfX = 0;
            int numPings = (int) Math.pow(Math.max(cols, rows), 2);
            for (int i = 0; i < numPings; i++) {
                String current = super.pingMap(d);
                if (current.equals("X")) numOfX++;
                if (numOfX > numPings / 2) {
                    walls.add(d);
                    return 10000.0;
                }
            }
            nonWalls.add(d);
        }
        return dx + dy + (-0.6) * Math.min(dx, dy);
    }

    //Generate adjacent points--- Doesn't remove walls, but does remove nulls.
    public List<Point> generateAdjacents(Point current) {
        Point nw = new Point((int) current.getX() - 1, (int) current.getY() - 1);
        Point ne = new Point((int) current.getX() - 1, (int) current.getY() + 1);
        Point n = new Point((int) current.getX() - 1, (int) current.getY());
        Point w = new Point((int) current.getX(), (int) current.getY() - 1);
        Point sw = new Point((int) current.getX() + 1, (int) current.getY() - 1);
        Point s = new Point((int) current.getX() + 1, (int) current.getY());
        Point se = new Point((int) current.getX() + 1, (int) current.getY() + 1);
        Point e = new Point((int) current.getX(), (int) current.getY() + 1);
        List<Point> adj = new ArrayList<>();
        Collections.addAll(adj, nw, ne, n, w, sw, s, se, e);

        // Remove the nodes that return null upon pinging--- Those are outside the boundaries of the map.
        adj.removeIf((Point p) -> p.getX() >= rows || p.getX() < 0 || p.getY() >= cols || p.getY() < 0);
        return adj;
    }


    //Take a Map of Point to Point (which theoretically would include all the mappings of node to node for correct path)
    // and construct a list from that Map up until the passed in current point.
    public List<Point> reconstructPath(Map<Point, Point> cameFrom, Point current) {
        List<Point> totalPath = new ArrayList<Point>();
        totalPath.add(current);
        while (cameFrom.keySet().contains(current)) {
            current = cameFrom.get(current);
            totalPath.add(current);
        }
        Collections.reverse(totalPath);
        return totalPath;
    }

    //Adapted from Stackoverflow:
    //http://stackoverflow.com/questions/1383797/java-hashmap-how-to-get-key-from-value/28415495#28415495
    // Look in a map and find a Point based on the Double value. In this case, that means we look through fScore table for a certain fScore
    // and find the point associated.
    public Point getPointFromFScore(double score) {
        return fScores.keySet().stream()
                .filter(p -> fScores.get(p).equals(score) && !evaluated.contains(p))
                .findAny()
                .orElse(null);
    }


    private void updateScores(Point current, Point neighbor, Point go, double gScore) {
        if (!notEvaluated.contains(neighbor)) {
            notEvaluated.add(neighbor);
        }
        cameFrom.put(neighbor, current);
        gScores.put(neighbor, gScore);
        double hScore = gScores.get(neighbor) + heuristic(neighbor, go);

        //Tiebreaking. This reduces this current path's fScore, because it's the most efficient thus far.
        while (fScores.values().contains(hScore)) {
            hScore *= 0.999;
        }
        fScores.put(neighbor, hScore);
    }

    //Based on pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm
    public List<Point> aStar(Point st, Point go) {

        //Lists of evaluated and not evaluated Points (which are the nodes in this case)
        evaluated = new ArrayList<>();
        notEvaluated = new ArrayList<>();
        notEvaluated.add(st);

        walls = new ArrayList<>();
        nonWalls = new ArrayList<>();

        //Key Value pairs of Point to Point. When this is full, it essentially has the moves the robot should make.
        cameFrom = new HashMap<>();

        //Map of g scores, initialized to postive infinity for every Point
        gScores = new HashMap<>();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                gScores.put(new Point(i, j), Double.POSITIVE_INFINITY);
            }
        }
        //Cost of start going to start is zero.
        gScores.put(st, 0.0);

        //Map of f scores, initialized to positive infinity for every point
        fScores = new HashMap<>();
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                fScores.put(new Point(i, j), Double.POSITIVE_INFINITY);
            }
        }
        //Cost of start going to goal as estimated by the heuristic initially.
        fScores.put(st, heuristic(st, go));

        // While there's still nodes to be evaluated, keep evaluating.
        while (!notEvaluated.isEmpty()) {

            // Find node with the lowest score.
            double lowestCurrentScore = Collections.min(fScores.values());
            Point current = getPointFromFScore(lowestCurrentScore);

            // If the current point doesn't exist, something's really wrong! Break.
            if (current == null) {
                break;
            }

            // If current node is equals goal, then we've generated a full path, and can go reconstruct it into a list.
            if ((int) current.getX() == (int) go.getX() && (int) current.getY() == (int) go.getY()) {
                return reconstructPath(cameFrom, go);
            }

            // Add current node to evaluated and take it from notEvaluated.
            if (notEvaluated.contains(current)) {
                notEvaluated.remove(current);
            }
            if (!evaluated.contains(current)) {
                evaluated.add(current);
            }

            //Generate adjacent nodes of current node.
            List<Point> adj = generateAdjacents(current);

            //Now, for each adjacent node to the current, evaluate the fScores and gScores.
            double gScore;
            for (Point neighbor : adj) {
                if (evaluated.contains(neighbor)) {
                    continue;
                }

                gScore = gScores.get(current) + heuristic(current, neighbor);

                if (!notEvaluated.contains(neighbor)) {
                    notEvaluated.add(neighbor);
                } else if (gScore >= gScores.get(neighbor)) {
                    continue;
                }
                if (isUncertain) {
                    if (!walls.contains(neighbor)) {
                        updateScores(current, neighbor, go, gScore);
                    }
                } else {
                    if (!super.pingMap(neighbor).equals("X")) {
                        updateScores(current, neighbor, go, gScore);
                    }
                }
            }
            fScores.remove(current);
        }
        // No path generated, return empty list.
        return new ArrayList<>();
    }
}
