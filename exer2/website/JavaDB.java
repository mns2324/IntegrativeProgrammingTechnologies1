package javadb;

import java.util.ArrayList;
import java.util.List;
import static javadb.DBConnect.rs;

import java.security.MessageDigest;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

/**
 * JavaDB.java
 * Extends DBConnect to provide data access methods for the Students table.
 * This class is compiled into a JAR, then converted to a .NET DLL via IKVM,
 * allowing ASP.NET (C#) to call these Java methods directly.
 *
 * The generated DLL is then referenced in the ASP.NET project.
 */
public class JavaDB extends DBConnect {
    
    private String hashPassword(String password) {
        try {
            // hash the incoming plaintext password before comparing
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashed = md.digest(password.getBytes("UTF-8"));
            // convert bytes to lowercase hex string
            StringBuilder sb = new StringBuilder();
            for (byte b : hashed) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception ex) {
            System.out.println("Hash error: " + ex);
            return null;
        }
    }
    
    public boolean registerUser(String fullname, String username, String password, String role, String contact, String address) {
        try {
            String sql
                    = "INSERT INTO users "
                    + "(full_name, username, password, role, contact_number, address) "
                    + "VALUES (?, ?, ?, ?, ?, ?)";
            PreparedStatement ps = con.prepareStatement(sql);

            // password is hashed here
            ps.setString(1, fullname);
            ps.setString(2, username);
            ps.setString(3, hashPassword(password));
            ps.setString(4, role);
            ps.setString(5, contact);
            ps.setString(6, address);

            int rows = ps.executeUpdate();
            System.out.println("Rows inserted: " + rows);
            return rows > 0;

        } catch (Exception ex) {
            System.out.println("Register Error: " + ex);
            return false;
        }
    }

    public String[] loginUser(String username, String password) {
        try {          
            String hashedInput = hashPassword(password);

            String sql = "SELECT user_id, full_name, role FROM users WHERE username = ? AND password = ?";
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, username);
            ps.setString(2, hashedInput);
            ResultSet rs = ps.executeQuery();

            if (rs.next())
                return new String[]{ rs.getString("user_id"), rs.getString("full_name"), rs.getString("role") };

        } catch (Exception e) { 
            System.out.println("Login Error: " + e);
            return null;
        }
        return null;
    }

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
                String[] row = new String[7];
                row[0] = rs.getString("fruit_id");
                row[1] = rs.getString("fruit_name");
                row[2] = rs.getString("category");
                row[3] = rs.getString("price");
                row[4] = rs.getString("stock_quantity");
                row[5] = rs.getString("image_path");
                row[6] = "actions"; // placeholder so C# knows this column exists
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
    
    public String[] getMachineStatus() {
        try {
            // ORDER BY id DESC LIMIT 1 gets the most recent row inserted by python
            String query = "SELECT conveyor1_status, conveyor2_status, current_box_position, " +
                           "arduino_status, last_updated " +
                           "FROM machine_status ORDER BY status_id DESC LIMIT 1";
            java.sql.ResultSet statusRs = st.executeQuery(query);

            if (statusRs.next()) {
                String[] row = new String[5];
                row[0] = statusRs.getString("conveyor1_status");
                row[1] = statusRs.getString("conveyor2_status");
                row[2] = statusRs.getString("current_box_position");
                row[3] = statusRs.getString("arduino_status");
                row[4] = statusRs.getString("last_updated");
                return row;
            }
        } catch (Exception e) {
            System.out.println("Error in getMachineStatus(): " + e);
        }
        return new String[] { "unknown", "unknown", "unknown", "offline", "never" };
    }
    
    public String[][] getPendingOrders() {
        // code for exer 3 here, interact with python kivy app
        return null;
    }

    /**
     * updates an existing fruit record by fruit_id
     */
    public String updateFruit(String fruitId, String fruitName, String category, String price, String stockQuantity, String imagePath) {
        try {
            // none of the fields should be blank
            if (fruitName == null || fruitName.trim().isEmpty())        return "ERROR: Fruit name is required.";
            if (category == null || category.trim().isEmpty())          return "ERROR: Category is required.";
            if (price == null || price.trim().isEmpty())                return "ERROR: Price is required.";
            if (stockQuantity == null || stockQuantity.trim().isEmpty())return "ERROR: Quantity is required.";

            // validate that price is a valid decimal
            double parsedPrice;
            try { 
                parsedPrice = Double.parseDouble(price.trim()); 
            }
            catch (NumberFormatException ex) { 
                return "ERROR: Price must be a valid decimal (e.g. 20.00)."; 
            }
            if (parsedPrice < 0) return "ERROR: Price cannot be negative.";

            // validate that stock quantity is a valid integer
            int parsedQty;
            try { 
                parsedQty = Integer.parseInt(stockQuantity.trim()); 
            }
            catch (NumberFormatException ex) { 
                return "ERROR: Quantity must be a whole number."; 
            }
            if (parsedQty < 0) return "ERROR: Quantity cannot be negative.";

            String query =
                "UPDATE fruits SET " +
                "fruit_name = ?,  category = ?, price = ?, " +
                "stock_quantity = ?, image_path = ? " +
                "WHERE fruit_id = ?";

            java.sql.PreparedStatement ps = con.prepareStatement(query);
            ps.setString(1, fruitName.trim());
            ps.setString(2, category.trim());
            ps.setDouble(3, parsedPrice);
            ps.setInt   (4, parsedQty);
            ps.setString(5, imagePath  != null ? imagePath.trim() : "");
            ps.setInt   (6, Integer.parseInt(fruitId.trim()));
            ps.executeUpdate();
            ps.close();

            return "OK";
        } catch (Exception e) {
            return "ERROR: " + e.getMessage();
        }
    }

    /**
     * deletes a fruit record by fruit_id
     */
    public String deleteFruit(String fruitId) {
        try {
            int id = Integer.parseInt(fruitId.trim());

            // check if any sorting logs reference this fruit
            String checkQuery = "SELECT COUNT(*) FROM sorting_logs WHERE fruit_id = ?";
            java.sql.PreparedStatement psCheck = con.prepareStatement(checkQuery);
            psCheck.setInt(1, id);
            java.sql.ResultSet checkRs = psCheck.executeQuery();
            checkRs.next();
            int logCount = checkRs.getInt(1);
            psCheck.close();

            if (logCount > 0) {
                return "ERROR: Cannot delete Fruit #" + fruitId + "; it has " 
                    + logCount + " sorting log(s) referencing it. Delete those logs first.";
            }

            // safe to delete
            String deleteFruit = "DELETE FROM fruits WHERE fruit_id = ?";
            java.sql.PreparedStatement psFruit = con.prepareStatement(deleteFruit);
            psFruit.setInt(1, id);
            psFruit.executeUpdate();
            psFruit.close();

            return "OK";
        } catch (Exception e) {
            return "ERROR: " + e.getMessage();
        }
    }
    
    // sample test for exer 3
    public static void main(String[] args) {
//        JavaDB db = new JavaDB();
//
//        db.Connect();
//
//        boolean success = db.registerUser(
//                "Juan Dela Cruz",
//                "juan123456",
//                "mypassword",
//                "customer",
//                "09171234567",
//                "Davao City"
//        );
//
//        if (success) {
//            System.out.println("Registration successful");
//        } else {
//            System.out.println("Registration failed");
//        }
    }
}

