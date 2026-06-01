/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javasamplecode;

import java.util.ArrayList;
import java.util.List;

public class JavaApplication2 extends DBConnect {
    
    
    public String[][] getData(){
        List<String[]> products = new ArrayList<>();
        try{
            String query;
                query = "select studid, studname, studcrs, studgender, yrlvl from students";
            rs = st.executeQuery(query);
            while (rs.next()){
                String[] product = new String[5];
                product[0] = rs.getString("studid");
                product[1] = rs.getString("studname");
                product[2] = rs.getString("studcrs");
                product[3] = rs.getString("studgender");
                product[4] = rs.getString("yrlvl");
                products.add(product);
            }
        }
        catch(Exception e){
            System.out.println("Error:" + e);
        }
        return products.toArray(new String[0][0]);
    }    
    
    
    public String getName() {
        return "John";
    }
    public void SaveRecord(int studid,String studname,String studcrs,String studgender,String yrlvl) {
        JavaApplication2 s = new JavaApplication2();
        // CONNECT DATABASE
        s.Connect();
        try {

            String query =
                    "INSERT INTO students " +
                    "(studid, studname, studcrs, studgender, yrlvl) " +
                    "VALUES (" +
                    studid + ", '" +
                    studname + "', '" +
                    studcrs + "', '" +
                    studgender + "', '" +
                    yrlvl + "')";

            s.st.executeUpdate(query);

            System.out.println("Record Saved!");

        } catch (Exception ex) {

            System.out.println(ex);
        }
    }
    
    public static void main(String[] args) {
        JavaApplication2 s = new JavaApplication2();
          s.SaveRecord(
                1001,
                "Juan Dela Cruz",
                "BSIT",
                "Male",
                "1st Year"
        );      
    }
    
}
