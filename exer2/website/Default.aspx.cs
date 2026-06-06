/*
 * Default.aspx.cs
 * Code-behind for the Student Record System web form.
 *
 * HOW THE JAVA INTEGRATION WORKS (IKVM):
 * ─────────────────────────────────────────────────────────────────────────────
 * 1. The Java classes (DBConnect.java + JavaApplication2.java) are compiled
 *    into a JAR file using javac / NetBeans / your IDE.
 *
 * 2. IKVM converts the JAR + MySQL connector JAR into a .NET DLL:
 *
 *      ikvmc -target:library JavaApplication2.jar mysql-connector-java-X.X.X.jar
 *
 *    This produces:  JavaApplication2.dll
 *
 * 3. That DLL is added as a Reference in this ASP.NET project
 *    (right-click References → Add Reference → Browse → JavaApplication2.dll).
 *
 * 4. The using directive below pulls in the Java package namespace:
 *      using javaapplication2;
 *
 * 5. C# can now instantiate JavaApplication2 and call Connect(), getData(),
 *    SaveRecord(), getName() — exactly as if they were written in C#.
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * REQUIRED REFERENCES in this project:
 *   - JavaApplication2.dll   (IKVM-converted from your JAR)
 *   - IKVM.OpenJDK.Core.dll  (and other IKVM runtime DLLs — install via NuGet:
 *                              Install-Package IKVM)
 */

using System;
using System.Web.UI;
using javadb;          // ← namespace from the IKVM-converted Java DLL

namespace WebApplication8
{
    public partial class WebForm1 : System.Web.UI.Page
    {
        // ── Instantiate the Java class (via IKVM DLL) ──────────────────────────
        // This is a real Java object, IKVM makes it look like a C# class.
        private JavaDB javaApp = new JavaDB();

        // ──────────────────────────────────────────────────────────────────────
        // PAGE LOAD
        // Runs every time the page is loaded or refreshed 
        // ──────────────────────────────────────────────────────────────────────
        protected void Page_Load(object sender, EventArgs e)
        {
            javaApp.Connect();

            // fetch all student records via the Java getData() method
            // getData() returns a String[][] (Java 2D array → C# string[][])
            string[][] data = javaApp.getData();

            // render the data as an HTML table into litTable
            DisplayStudentTable(data);           
        }

        // ──────────────────────────────────────────────────────────────────────
        // BUTTON CLICK — Save Record
        // Calls the Java SaveRecord() method, then refreshes the table.
        // ──────────────────────────────────────────────────────────────────────
        protected void Button1_Click(object sender, EventArgs e)
        {
            int studentId;
            if (!int.TryParse(txtid.Text.Trim(), out studentId))
            {
                litStatus.Text = StatusAlert("danger", "&#9888; Student ID must be a number.");
                return;
            }

            try
            {
                javaApp.Connect();
                // ── Call the Java SaveRecord() method via IKVM ──────────────────
                javaApp.SaveRecord(
                    studentId,
                    txtname.Text.Trim(),
                    txtcourse.Text.Trim(),
                    txtgender.Text.Trim(),
                    txtyear.Text.Trim()
                );

                // ── Refresh the student list ────────────────────────────────────
                string[][] data = javaApp.getData();
                DisplayStudentTable(data);

                // ── Confirm with a status message ───────────────────────────────
                litStatus.Text = StatusAlert("success", "Record saved! ID was: " + studentId);

                // Clear the form fields after a successful save
                txtid.Text = "";
                txtname.Text = "";
                txtcourse.Text = "";
                txtgender.Text = "";
                txtyear.Text = "";
            }
            catch (Exception ex)
            {
                litStatus.Text = StatusAlert("danger", "ERROR: " + ex.Message + " | " + ex.ToString());
            }
        }

        // ──────────────────────────────────────────────────────────────────────
        // DISPLAY STUDENT TABLE
        // Converts the String[][] from Java getData() into a styled HTML table
        // and injects it into the <asp:Literal ID="litTable"> control.
        // ──────────────────────────────────────────────────────────────────────
        private void DisplayStudentTable(string[][] data)
        {
            if (data == null || data.Length == 0)
            {
                litTable.Text = @"
                    <div class='empty-state'>
                        &#128194; No student records found. Add one above.
                    </div>";
                return;
            }

            System.Text.StringBuilder sb = new System.Text.StringBuilder();

            sb.Append("<table class='data-table'>");

            // ── Table Header ──────────────────────────────────────────────────
            sb.Append("<thead><tr>");
            sb.Append("<th>#</th>");
            sb.Append("<th>Student ID</th>");
            sb.Append("<th>Full Name</th>");
            sb.Append("<th>Course</th>");
            sb.Append("<th>Gender</th>");
            sb.Append("<th>Year Level</th>");
            sb.Append("</tr></thead>");

            // ── Table Body ────────────────────────────────────────────────────
            sb.Append("<tbody>");

            int rowNum = 1;
            foreach (string[] row in data)
            {
                sb.Append("<tr>");
                sb.Append("<td style='color:#bbb;font-size:12px;'>" + rowNum++ + "</td>");

                // Student ID
                sb.Append("<td><strong>" + HtmlEncode(row[0]) + "</strong></td>");

                // Student Name
                sb.Append("<td>" + HtmlEncode(row[1]) + "</td>");

                // Course — badge style
                sb.Append("<td><span class='badge badge-green'>" + HtmlEncode(row[2]) + "</span></td>");

                // Gender — colour-coded badge
                string genderClass = (row[3] != null && row[3].ToLower().Contains("female")) ? "badge-pink" : "badge-blue";
                sb.Append("<td><span class='badge " + genderClass + "'>" + HtmlEncode(row[3]) + "</span></td>");

                // Year Level
                sb.Append("<td>" + HtmlEncode(row[4]) + "</td>");

                sb.Append("</tr>");
            }

            sb.Append("</tbody>");
            sb.Append("</table>");

            litTable.Text = sb.ToString();
        }

        // ──────────────────────────────────────────────────────────────────────
        // HELPERS
        // ──────────────────────────────────────────────────────────────────────

        /// <summary>Builds a styled alert HTML block.</summary>
        private string StatusAlert(string type, string message)
        {
            string bg    = type == "success" ? "#e8f5e9" : "#ffebee";
            string border = type == "success" ? "#43a047" : "#e53935";
            string color  = type == "success" ? "#2e7d32" : "#c62828";

            return string.Format(
                "<div style='margin-top:16px;padding:12px 16px;border-radius:6px;" +
                "background:{0};border-left:4px solid {1};color:{2};font-size:14px;'>{3}</div>",
                bg, border, color, message
            );
        }

        /// <summary>Escapes HTML special characters to prevent XSS.</summary>
        private string HtmlEncode(string input)
        {
            if (string.IsNullOrEmpty(input)) return "";
            return System.Web.HttpUtility.HtmlEncode(input);
        }
    }
}
