using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using javadb;

namespace KivyPostRequestReceiver
{
    public partial class Login : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            // get the data from the post request's dict
            string username = Request.Form["username"];
            string password = Request.Form["password"];

            if (username == null || password == null)
            {
                Response.Write("Missing credentials");
                Response.End();
                return;
            }

            try
            {
                JavaDB db = new JavaDB();
                db.Connect();
                string[] result = db.loginUser(username, password);

                // return "OK:user_id:fullname:role" so kivy can parse it
                Response.Write(result != null ? "OK:" + result[0] + ":" + result[1] + ":" + result[2] : "Invalid username or password");
            }
            catch (Exception ex)
            {
                Response.Write("Error: " + ex.Message);
            }
            Response.End();
        }
    }
}