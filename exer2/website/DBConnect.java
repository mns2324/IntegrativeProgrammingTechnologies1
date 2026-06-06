package javadb;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

/**
 * DBConnect.java
 * Base class that handles MySQL database connectivity.
 * Compiled into a JAR, then converted to a .NET DLL via IKVM.
 */
public class DBConnect {

    static Connection con;
    static Statement st;
    static ResultSet rs;

    /**
     * Opens a connection to the MySQL database.
     * Update host, port, database name, username, and password as needed.
     */
    public void Connect() {
        try {
            // load the MySQL JDBC driver
            Class.forName("com.mysql.jdbc.Driver");

            // establish connection 
            con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/sample",
                "root",
                "root"
            );

            con.setAutoCommit(true); 
            st = con.createStatement();
            System.out.println("Connected to database.");

        } catch (Exception ex) {
            System.out.println("Failed to Connect: " + ex);
        }
    }
}
