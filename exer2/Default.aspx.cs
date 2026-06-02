using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;


namespace WebApplication1
{
    public partial class _Default : System.Web.UI.Page
    {
        javasamplecode.JavaApplication2 app = new javasamplecode.JavaApplication2();

        protected void Page_Load(object sender, EventArgs e)
        {
            app.Connect();
            string[][] data = app.getData();
            DisplayDataInListView(data);
        }

        protected void Button1_Click(object sender, EventArgs e)
        {
            app.SaveRecord(
                Convert.ToInt32(txtid.Text),
                txtname.Text,
                txtcourse.Text,
                txtgender.Text,
                txtyear.Text
            );
            string[][] data = app.getData();
            DisplayDataInListView(data);
            Response.Write(app.getName());
        }

        private void DisplayDataInListView(string[][] data)
        {
            string html = "<table border='1' cellpadding='5'>";
            html += "<tr><th>Student ID</th><th>Student Name</th><th>Course</th><th>Gender</th><th>Year Level</th></tr>";
            foreach (var row in data)
            {
                html += "<tr>";
                foreach (var col in row)
                    html += "<td>" + col + "</td>";
                html += "</tr>";
            }
            html += "</table>";
            litTable.Text = html;
        }
    }
}