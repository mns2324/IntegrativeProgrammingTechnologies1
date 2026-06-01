/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javasamplecode;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
public class DBConnect {
    static Connection con;
    static Statement st;
    static ResultSet rs;  
    
public void Connect() {

    try {

        Class.forName("com.mysql.jdbc.Driver");

        con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/sample",
                "root",
                "root"
                        
        );

        st = con.createStatement();

        System.out.println("Connected");

    } catch (Exception ex) {

        System.out.println("Failed to Connect: " + ex);

    }


}    
}

