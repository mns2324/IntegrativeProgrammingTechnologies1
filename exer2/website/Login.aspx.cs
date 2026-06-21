using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using javadb; 

namespace SmartFruitInventorySystem
{
    public partial class Login : System.Web.UI.Page
    {
        private JavaDB javaApp = new JavaDB();

        protected void Page_Load(object sender, EventArgs e)
        {
            // redirect to dashboard if already logged in
            if (Request.Cookies["fruitUser"] != null)
                Response.Redirect("Dashboard.aspx");
        }

        protected void BtnLogin_Click(object sender, EventArgs e)
        {
            string user = txtUser.Text.Trim();
            string pass = txtPass.Text.Trim();           

            if (string.IsNullOrEmpty(user) || string.IsNullOrEmpty(pass))
            {
                ShowError("Please enter both username and password.");
                return;
            }

            javaApp.Connect(); // dont forget this lol

            // Returns string[] { full_name, role } on success, null on fail.
            string[] result = javaApp.loginUser(user, pass);

            if (result != null)
            {
                // set cookies
                SetCookie("fruitUser",     user);
                SetCookie("fruitFullName", result[0]); // full_name
                SetCookie("fruitRole",     result[1]); // admin or customer

                Response.Redirect("Dashboard.aspx");
            }
            else
            {
                ShowError("Invalid username or password. Please try again.");
            }
        }

        private void SetCookie(string name, string value)
        {
            Response.Cookies.Add(new HttpCookie(name, value)
            {
                Expires  = DateTime.Now.AddHours(2), 
                Path     = "/",
                HttpOnly = true
            });
        }

        private void ShowError(string msg)
        {
            litError.Text = "<div class='alert-error'>" +msg+ "</div>";
        }
    }
}