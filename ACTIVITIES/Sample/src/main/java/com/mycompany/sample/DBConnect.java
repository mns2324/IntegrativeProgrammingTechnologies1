package com.mycompany.sample;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class DBConnect {

    public static Connection con;
    public static Statement st;

    public static boolean connect() {

        try {

            Class.forName("com.mysql.jdbc.Driver");

            con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/sample?zeroDateTimeBehavior=convertToNull",
                "root",
                "root"
            );

            st = con.createStatement();

            System.out.println("Connected");

            return true;

        } catch (Exception ex) {

            System.out.println("Failed to Connect: " + ex);

            return false;
        }
    }
}