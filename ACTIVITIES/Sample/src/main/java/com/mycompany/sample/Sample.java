package com.mycompany.sample;

public class Sample {

    public void SaveRecord(int studid,String studname,String studadd,String studcrs,String studgender,String yrlvl) {
        try {
            String query =
                    "INSERT INTO students " +
                    "(studid, studname, studadd, studcrs, studgender, yrlvl) " +
                    "VALUES (" +
                    studid + ", '" +
                    studname + "', '" +
                    studadd + "', '" +
                    studcrs + "', '" +
                    studgender + "', '" +
                    yrlvl + "')";

            // cursor.execute()
            DBConnect.st.executeUpdate(query);
        } catch (Exception ex) {
            System.out.println(ex);
        }
    }
    
    public int EditRecord(int studid,String studname,String studadd,String studcrs,String studgender,String yrlvl){
        try {
            String query =
                "UPDATE students SET " +
                "studname='" + studname + "', " +
                "studadd='" + studadd + "', " +
                "studcrs='" + studcrs + "', " +
                "studgender='" + studgender + "', " +
                "yrlvl='" + yrlvl + "' " +
                "WHERE studid=" + studid;

            // cursor.execute(), also returns an int if assigned to a var
            int rowsAffected = DBConnect.st.executeUpdate(query);
            return rowsAffected;
        } catch (Exception ex) {
            System.out.println(ex);
            return 0;
        }
    }
    public int DeleteRecord(int studid){
        try {
            String query = "DELETE FROM students WHERE studid = " +studid;

            // cursor.execute(), also returns an int if assigned to a var
            int rowsAffected = DBConnect.st.executeUpdate(query);
            return rowsAffected;
        } catch (Exception ex) {
            System.out.println(ex);
            return 0;
        }
    }
    public String SearchRecord(int studid){
        try {
            String query = "SELECT * FROM students WHERE studid = " +studid;
            DBConnect.rs = DBConnect.st.executeQuery(query);

            if (DBConnect.rs.next()) {
                return DBConnect.rs.getInt("studid") + "|" +
                DBConnect.rs.getString("studname") + "|" +
                DBConnect.rs.getString("studadd") + "|" +
                DBConnect.rs.getString("studcrs") + "|" +
                DBConnect.rs.getString("studgender") + "|" +
                DBConnect.rs.getString("yrlvl");
            } else {
                return null;
            }
   
        } catch (Exception ex) {
            System.out.println(ex);
            return null;
        }
    }
    
    public String setName() {
        return "Ayet";
    }
    public String getName() {

        return "CCCCC";
    }
    
    // this executes if you run this class through java/netbeans (to test that the db connection works)
    // otherwise, this class is only used to call its methods in python
    public static void main(String[] args) {       
        // CONNECT DATABASE
        DBConnect.connect();
        Sample s = new Sample(); 
        // INSERT RECORD
        s.SaveRecord(
                1009,
                "Juan Dela Cruz",
                "Davao City",
                "BSIT",
                "Male",
                "1st Year"
        );
        // DISPLAY NAME
        System.out.println(s.getName());
    }
}