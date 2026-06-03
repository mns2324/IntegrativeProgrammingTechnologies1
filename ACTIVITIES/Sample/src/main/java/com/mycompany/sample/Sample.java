package com.mycompany.sample;

public class Sample {

    public void SaveRecord(
            int studid,
            String studname,
            String studadd,
            String studcrs,
            String studgender,
            String yrlvl
    ) {

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

            DBConnect.st.executeUpdate(query);

            System.out.println("Saved");

        } catch (Exception ex) {

            System.out.println(ex);
        }
    }
    public String setName() {

        return "Ayet";
    }
    public String getName() {

        return "CCCCC";
    }
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