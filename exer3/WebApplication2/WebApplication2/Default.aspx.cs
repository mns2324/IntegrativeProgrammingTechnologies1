using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using javaapplication2;

public partial class _Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        // read request post data
        string fullname = Request.Form["fullname"];
        string username = Request.Form["username"];
        string password = Request.Form["password"];
        string contact = Request.Form["contact"];
        string address = Request.Form["address"];
        if (fullname == null || username == null || password == null)
        {
            Response.Write("Missing required fields");
            return;
        }

        try
        {
            Javaapplication2 db = new Javaapplication2();
            db.Connect();
            bool result = db.RegisterUser(
                fullname,
                username,
                password,
                contact,
                address
            );
            // send response to iis depending on return value from java
            Response.Write(result ? "Registration successful" : "Registration failed");
        }
        catch (Exception ex)
        {
            Response.Write("Error: " + ex.Message);
        }
    }
}