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
     * Retrieves all student records from the database.
     * @return 2D String array: each row = { studid, studname, studcrs, studgender, yrlvl }
     */
    public String[][] getData() {
        List<String[]> students = new ArrayList<>();
        try {
            String query = "SELECT studid, studname, studcrs, studgender, yrlvl FROM students";
            rs = st.executeQuery(query);

            while (rs.next()) {
                String[] row = new String[5];
                row[0] = rs.getString("studid");
                row[1] = rs.getString("studname");
                row[2] = rs.getString("studcrs");
                row[3] = rs.getString("studgender");
                row[4] = rs.getString("yrlvl");
                students.add(row);
            }
        } catch (Exception e) {
            System.out.println("Error in getData(): " + e);
        }
        return students.toArray(new String[0][0]);
    }

    /**
     * Saves a new student record to the database.
     * NOTE: Uses string concatenation — consider using PreparedStatement in production.
     *
     * @param studid     Unique student ID
     * @param studname   Full name of the student
     * @param studcrs    Course / program enrolled
     * @param studgender Gender of the student
     * @param yrlvl      Year level (e.g., "1st Year")
     */
    public void SaveRecord(int studid, String studname, String studcrs, String studgender, String yrlvl) {
        try {
            String query =
                "INSERT INTO students (studid, studname, studcrs, studgender, yrlvl) " +
                "VALUES (" +
                studid + ", '" +
                studname + "', '" +
                studcrs + "', '" +
                studgender + "', '" +
                yrlvl + "')";
            st.executeUpdate(query);
            System.out.println("Record saved successfully.");
        } catch (Exception ex) {
            System.out.println("Error in SaveRecord(): " + ex);
        }
    }

    /**
     * Main method for standalone Java testing (not used by ASP.NET).
     */
    public static void main(String[] args) {
        JavaDB s = new JavaDB();
        s.Connect();
        s.SaveRecord(1007, "Juan Dela Cruz", "BSIT", "Male", "1st Year");

        String[][] data = s.getData();
        for (String[] row : data) {
            for (String col : row) {
                System.out.print(col + "\t");
            }
            System.out.println();
        }
    }
}

