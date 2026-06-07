/*
 * Default.aspx.cs
 * Code-behind for the Fruit Inventory system web form.
 */

using System;
using System.Web.UI;
using javadb; // namespace from the IKVM-converted Java DLL

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
            string[][] fruitrecords = javaApp.getFruitInventory();
            string[][] logrecords = javaApp.getSortingLogs();

            // render the data as an HTML table into the litTable
            DisplayFruitInventory(fruitrecords);
            DisplaySortingLogs(logrecords);
        }

        // ──────────────────────────────────────────────────────────────────────
        // BUTTON CLICK — Save Record
        // Calls the Java SaveRecord() method, then refreshes the table.
        // ──────────────────────────────────────────────────────────────────────
        protected void Button1_Click(object sender, EventArgs e)
        {
            //int studentId;
            //if (!int.TryParse(txtid.Text.Trim(), out studentId))
            //{
            //    litStatus.Text = StatusAlert("danger", "&#9888; Student ID must be a number.");
            //    return;
            //}

            //try
            //{
            //    javaApp.Connect();
            //    // ── Call the Java SaveRecord() method via IKVM ──────────────────
            //    javaApp.SaveRecord(
            //        studentId,
            //        txtname.Text.Trim(),
            //        txtcourse.Text.Trim(),
            //        txtgender.Text.Trim(),
            //        txtyear.Text.Trim()
            //    );

            //    // ── Refresh the student list ────────────────────────────────────
            //    string[][] data = javaApp.getData();
            //    DisplayStudentTable(data);

            //    // ── Confirm with a status message ───────────────────────────────
            //    litStatus.Text = StatusAlert("success", "Record saved! ID was: " + studentId);

            //    // Clear the form fields after a successful save
            //    txtid.Text = "";
            //    txtname.Text = "";
            //    txtcourse.Text = "";
            //    txtgender.Text = "";
            //    txtyear.Text = "";
            //}
            //catch (Exception ex)
            //{
            //    litStatus.Text = StatusAlert("danger", "ERROR: " + ex.Message + " | " + ex.ToString());
            //}
        }

        // ──────────────────────────────────────────────────────────────────────
        // DISPLAY FRUITS TABLE
        // Converts the String[][] from Java getFruitInventory() into a styled HTML table
        // and injects it into the <asp:Literal ID="litTable"> control.
        // ──────────────────────────────────────────────────────────────────────
        private void DisplayFruitInventory(string[][] data)
        {
//            if (data == null || data.Length == 0)
//            {
//                litTable.Text = @"
//                    <div class='empty-state'>
//                        &#128194; No fruits were found.
//                    </div>";
//                return;
//            }

            System.Text.StringBuilder sb = new System.Text.StringBuilder();

            sb.Append("<table class='data-table'>");

            // ── Table Header ──────────────────────────────────────────────────
            sb.Append("<thead><tr>");
            sb.Append("<th>Image</th>");
            sb.Append("<th>ID</th>");
            sb.Append("<th>Name</th>");
            sb.Append("<th>Category</th>");
            sb.Append("<th>Price</th>");
            sb.Append("<th>Quantity</th>");          
            sb.Append("</tr></thead>");

            // ── Table Body ────────────────────────────────────────────────────
            sb.Append("<tbody>");

            foreach (string[] row in data)
            {
                sb.Append("<tr>");

                // 1 - Image
                // 2 - Fruit ID
                // 3 - Fruit Name
                // 4 - Category
                // 5 - Price
                // 6 - Quantity
                sb.Append("<td><img src='" + HtmlEncode(row[5]) + "' alt='" + HtmlEncode(row[1]) + "' class='fruit-img'/></td>"); 
                sb.Append("<td><strong>" + HtmlEncode(row[0]) + "</strong></td>");
                sb.Append("<td>" + HtmlEncode(row[1]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[2]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[3]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[4]) + "</td>");

                // string genderClass = (row[3] != null && row[3].ToLower().Contains("female")) ? "badge-pink" : "badge-blue";
                // sb.Append("<td><span class='badge " + genderClass + "'>" + HtmlEncode(row[3]) + "</span></td>");
                sb.Append("</tr>");
            }

            sb.Append("</tbody>");
            sb.Append("</table>");

            litFruitsTable.Text = sb.ToString();
        }

        // ──────────────────────────────────────────────────────────────────────
        // DISPLAY SORTING LOGS
        // Converts the String[][] from Java getSortingLogs() into a styled HTML table
        // and injects it into the <asp:Literal ID="litTable"> control.
        // ──────────────────────────────────────────────────────────────────────
        private void DisplaySortingLogs(string[][] data)
        {
//            if (data == null || data.Length == 0)
//            {
//                litTable.Text = @"
//                    <div class='empty-state'>
//                        &#128194; No sorting logs found. 
//                    </div>";
//                return;
//            }

            System.Text.StringBuilder sb = new System.Text.StringBuilder();

            sb.Append("<table class='data-table'>");

            // ── Table Header ──────────────────────────────────────────────────
            sb.Append("<thead><tr>");
            sb.Append("<th>Log ID</th>");
            sb.Append("<th>Detected Label</th>");
            sb.Append("<th>Confidence</th>");
            sb.Append("<th>Detection Date/Time</th>");
            sb.Append("<th>Conveyor Action</th>");
            sb.Append("</tr></thead>");

            // ── Table Body ────────────────────────────────────────────────────
            sb.Append("<tbody>");

            foreach (string[] row in data)
            {
                sb.Append("<tr>");

                // important: fruit id is omitted even though it exists in the table
                // 1 - Log ID
                // 2 - Detected Label
                // 3 - Confidence Score
                // 4 - Detection Date/Time
                // 5 - Conveyor Action
                sb.Append("<td><strong>" + HtmlEncode(row[0]) + "</strong></td>");
                sb.Append("<td>" + HtmlEncode(row[1]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[2]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[3]) + "</td>");
                sb.Append("<td>" + HtmlEncode(row[4]) + "</td>");

                sb.Append("</tr>");
            }

            sb.Append("</tbody>");
            sb.Append("</table>");

            litLogsTable.Text = sb.ToString();
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
