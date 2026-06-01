using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using JavaApplication2;

namespace WebApplication1
{
    public partial class WebForm1 : System.Web.UI.Page
    {
        JavaApplication2 java = new JavaApplication2();
        protected void Page_Load(object sender, EventArgs e)
        {
            java.Connect();
            string[][] data = java.getData();
            DisplayDataInListView(data);
        }
        protected void Button1_Click(object sender, EventArgs e)
        {

            java.SaveRecord(Convert.ToInt32(txtid.Text), txtname.Text, txtcourse.Text, txtgender.Text, txtyear.Text);
            string[][] data = java.getData();
            DisplayDataInListView(data);
            Response.Write(java.getName());
        }
        private void DisplayDataInListView(string[][] data)
        {
            string html = "";

            html += "<table border='1' cellpadding='5'>";

            html += "<tr>";
            html += "<th>Student ID</th>";
            html += "<th>Student Name</th>";
            html += "<th>Course</th>";
            html += "<th>Gender</th>";
            html += "<th>Year Level</th>";
            html += "</tr>";

            foreach (var row in data)
            {
                html += "<tr>";

                foreach (var col in row)
                {
                    html += "<td>" + col + "</td>";
                }

                html += "</tr>";
            }

            html += "</table>";

            litTable.Text = html;
        }
    }


}