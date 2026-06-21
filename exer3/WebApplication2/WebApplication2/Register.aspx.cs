using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using javadb;

namespace KivyPostRequestReceiver
{
    public partial class Register : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            // get the data from the post request's dict
            string fullname = Request.Form["fullname"];
            string username = Request.Form["username"];
            string password = Request.Form["password"];
            string role = Request.Form["role"];
            string contact = Request.Form["contact"];
            string address = Request.Form["address"];
            if (fullname == null || username == null || password == null)
            {
                Response.Write("Missing required fields");
                Response.End();
                return;
            }

            try
            {
                JavaDB db = new JavaDB();
                db.Connect();
                bool result = db.registerUser(fullname, username, password, role, contact, address);
                // update kivy text if java returned >0 rows
                Response.Write(result ? "Registration successful" : "Registration failed");
            }
            catch (Exception ex)
            {
                Response.Write("Error: " + ex.Message);
            }
            Response.End();
        }
    }
}

