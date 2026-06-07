package javadb;

import java.util.ArrayList;
import java.util.List;
import static javadb.DBConnect.rs;

/**
 * JavaDB.java
 * Extends DBConnect to provide data access methods for the Students table.
 * This class is compiled into a JAR, then converted to a .NET DLL via IKVM,
 * allowing ASP.NET (C#) to call these Java methods directly.
 *
 * The generated DLL is then referenced in the ASP.NET project.
 */
public class JavaDB extends DBConnect {

    /**
     * retrieve all fruit records from the db,
     * returns a 2D string array.
     */
    public String[][] getFruitInventory() {
        List<String[]> fruits = new ArrayList<>();
        try {
            String query = "SELECT * FROM fruits";
            rs = st.executeQuery(query);

            while (rs.next()) {
                String[] row = new String[6];
                row[0] = rs.getString("fruit_id");
                row[1] = rs.getString("fruit_name");
                row[2] = rs.getString("category");
                row[3] = rs.getString("price");
                row[4] = rs.getString("stock_quantity");
                row[5] = rs.getString("image_path");
                fruits.add(row);
            }
        } catch (Exception e) {
            System.out.println("Error in Java getFruitInventory(): " + e);
        }
        return fruits.toArray(new String[0][0]);
    }
    
    /**
     * retrieve all sorting logs from the db,
     * returns a 2D string array.
     */
    public String[][] getSortingLogs() {
        List<String[]> sortinglogs = new ArrayList<>();
        try {
            // display latest logs at the top
            String query = "SELECT * FROM sorting_logs ORDER BY log_id DESC";
            rs = st.executeQuery(query);

            while (rs.next()) {
                // fruit_id omitted since its not really useful here
                String[] row = new String[5];
                row[0] = rs.getString("log_id");
                row[1] = rs.getString("detected_label");
                row[2] = rs.getString("confidence_score");
                row[3] = rs.getString("detection_datetime");
                row[4] = rs.getString("conveyor_action");
                sortinglogs.add(row);
            }
        } catch (Exception e) {
            System.out.println("Error in Java getSortingLogs(): " + e);
        }
        return sortinglogs.toArray(new String[0][0]);
    }
    
    public String[][] getPendingOrders() {
        // code for exer 3 here, interact with python kivy app
        return null;
    }

    /**
     * Saves a new student record to the database.
     */
//    public void SaveRecord(int studid, String studname, String studcrs, String studgender, String yrlvl) {
//        try {
//            String query =
//                "INSERT INTO students (studid, studname, studcrs, studgender, yrlvl) " +
//                "VALUES (" +
//                studid + ", '" +
//                studname + "', '" +
//                studcrs + "', '" +
//                studgender + "', '" +
//                yrlvl + "')";
//            st.executeUpdate(query);
//            System.out.println("Record saved successfully.");
//        } catch (Exception ex) {
//            System.out.println("Error in SaveRecord(): " + ex);
//        }
//    }

    /**
     * Main method for standalone Java testing (not used by ASP.NET).
     */
    public static void main(String[] args) {
//        JavaDB s = new JavaDB();
//        s.Connect();
//        s.SaveRecord(1007, "Juan Dela Cruz", "BSIT", "Male", "1st Year");
//
//        String[][] data = s.getData();
//        for (String[] row : data) {
//            for (String col : row) {
//                System.out.print(col + "\t");
//            }
//            System.out.println();
//        }
    }
}

