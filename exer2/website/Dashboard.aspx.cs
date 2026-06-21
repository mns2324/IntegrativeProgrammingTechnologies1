/*
 * Default.aspx.cs
 * Code-behind for the Fruit Inventory system web form.
 */

using System;
using System.Web.UI;
using javadb; // namespace from the IKVM-converted Java DLL

namespace SmartFruitInventorySystem
{
    public partial class Dashboard : System.Web.UI.Page
    {
        // ── Instantiate the Java class (via IKVM DLL) ──────────────────────────
        // This is a real Java object, IKVM makes it look like a C# class.
        private JavaDB javaApp = new JavaDB();

        // runs on every page load/refresh
        protected void Page_Load(object sender, EventArgs e)
        {
            // redirect back to login if this cookie isnt found
            if (Request.Cookies["fruitUser"] == null)
            {
                Response.Redirect("Login.aspx");
            }

            javaApp.Connect();
            RefreshTables();     
        }

        protected void BtnLogout_Click(object sender, EventArgs e)
        {
            // expire the cookie immediately then go back to login page
            var kill = new System.Web.HttpCookie("fruitUser", "")
            {
                Expires = DateTime.Now.AddHours(-1), 
                Path = "/"
            };
            Response.Cookies.Add(kill);
            Response.Redirect("Login.aspx");
        }

        private void RefreshTables()
        {
            // fetch all student records via the Java getFruitInventory()/getSortingLogs function,
            // then render the data as an HTML table into the litTable
            // both functions returns a String[][] (Java 2D array → C# string[][])
            DisplayFruitInventory(javaApp.getFruitInventory());
            DisplaySortingLogs(javaApp.getSortingLogs());
            DisplayMachineStatus(javaApp.getMachineStatus());
        }

        // read the fruit id and the new edited values then passes it to javaApp.editFruit() which runs the update query
        protected void BtnEdit_Click(object sender, EventArgs e)
        {
            string id = hfEditId.Value.Trim();
            string result = javaApp.updateFruit(
                id,
                hfEditName.Value.Trim(),
                hfEditCategory.Value.Trim(),
                hfEditPrice.Value.Trim(),
                hfEditQty.Value.Trim(),
                hfEditImage.Value.Trim()
            );

            litStatus.Text = result == "OK"
                ? StatusAlert("success", "Fruit #" + id + " updated successfully.")
                : StatusAlert("danger", result);

            RefreshTables();
        }

        // read the fruit id from hfDeleteId then passes it to javaApp.deleteFruit() which runs the delete query
        protected void BtnDelete_Click(object sender, EventArgs e)
        {
            string id = hfDeleteId.Value.Trim();
            string result = javaApp.deleteFruit(id);

            litStatus.Text = result == "OK"
                ? StatusAlert("success", "&#10003; Fruit #" + id + " deleted.")
                : StatusAlert("danger", result);

            RefreshTables();
        }
        // ──────────────────────────────────────────────────────────────────────
        // DISPLAY FRUITS TABLE
        // Converts the String[][] from Java getFruitInventory() into a styled HTML table
        // and injects it into the <asp:Literal ID="litTable"> control.
        // ──────────────────────────────────────────────────────────────────────
        private void DisplayFruitInventory(string[][] data)
        {
            if (data == null || data.Length == 0)
            {
                litFruitsTable.Text = @"
                    <div class='empty-state'>
                        &#128194; No fruits found. Insert one through SQL. 
                    </div>";
                litTotalFruits.Text = "<div class='card-value' style='color:green'>0</div>";
                return;
            }

            int totalQty = 0;
            var sb = new System.Text.StringBuilder();
            sb.Append("<table class='data-table'><thead><tr>");
            sb.Append("<th>Image</th>");
            sb.Append("<th>ID</th>");
            sb.Append("<th>Name</th>");
            sb.Append("<th>Category</th>");
            sb.Append("<th>Price</th>");
            sb.Append("<th>Quantity</th>");
            sb.Append("<th>Actions</th>");
            sb.Append("</tr></thead>");

            sb.Append("<tbody>");
            foreach (string[] row in data)
            {
                // row[0]=fruit_id  
                // [1]=fruit_name  
                // [2]=category
                // [3]=price     
                // [4]=stock_qty   
                // [5]=image_path
                string id = HtmlEncode(row[0]);
                string name = HtmlEncode(row[1]);
                string cat = HtmlEncode(row[2]);
                string price = HtmlEncode(row[3]);
                string qty = HtmlEncode(row[4]);
                string img = HtmlEncode(row[5]);

                // JS-safe (for onclick attribute values); escape single quotes
                string js1 = (row[1] ?? "").Replace("'", "\\'");
                string js2 = (row[2] ?? "").Replace("'", "\\'");
                string js3 = (row[3] ?? "").Replace("'", "\\'");
                string js4 = (row[4] ?? "").Replace("'", "\\'");
                string js5 = (row[5] ?? "").Replace("'", "\\'");

                // safely parse quantity, skip row if it's not a valid number
                int parsedQty;
                if (int.TryParse(row[4], out parsedQty))
                    totalQty += parsedQty;

                sb.Append("<tr id='row-" + id + "'>");
                sb.Append("<td><img src='" + img + "' alt='" + name + "' class='fruit-img'/></td>");
                sb.Append("<td><strong>" + id + "</strong></td>");
                sb.Append("<td>" + name + "</td>");
                sb.Append("<td>" + cat + "</td>");
                sb.Append("<td>" + price + "</td>");
                sb.Append("<td>" + qty + "</td>");
            
                sb.Append("<td>");
                // edit button passes all current values to JS editFruit()
                sb.AppendFormat(
                    "<button class='edit-btn' onclick=\"editFruit('{0}','{1}','{2}','{3}','{4}','{5}'); return false;\">&#9998; Edit</button> ",
                    id, js1, js2, js3, js4, js5
                );
                sb.Append("<button class='delete-btn' onclick=\"deleteFruit('" + id + "'); return false;\">Delete</button>");
                sb.Append("</td>");
                sb.Append("</tr>");
            }

            sb.Append("</tbody></table>");
            litFruitsTable.Text = sb.ToString();

            // update the stat card
            litTotalFruits.Text = "<div class='card-value' style='color:green'>" + totalQty + "</div>";
        }

        // ──────────────────────────────────────────────────────────────────────
        // DISPLAY SORTING LOGS
        // Converts the String[][] from Java getSortingLogs() into a styled HTML table
        // and injects it into the <asp:Literal ID="litTable"> control.
        // ──────────────────────────────────────────────────────────────────────
        private void DisplaySortingLogs(string[][] data)
        {
            if (data == null || data.Length == 0)
            {
                litLogsTable.Text = @"
                    <div class='empty-state'>
                        &#128194; No sorting logs found. Run the recognition python file and use your webcam to detect a fruit. 
                    </div>";
                return;
            }

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

        private void DisplayMachineStatus(string[] status)
        {
            // status[0] = conveyor1_status
            // status[1] = conveyor2_status
            // status[2] = current_box_position
            // status[3] = arduino_status
            // status[4] = last_updated

            // ── Top stat card: just arduino_status ───────────────────────────────
            bool arduinoOnline = status[3] == "online";
            string statColor = arduinoOnline ? "green" : "#c62828";
            litMachineStatus.Text = string.Format(
                "<div class='card-value' style='color:{0}'>{1}</div>",
                statColor, HtmlEncode(status[3]).ToUpper()
            );

            // ── Machine Monitoring card: full breakdown ───────────────────────────
            var sb = new System.Text.StringBuilder();
            sb.Append("<div style='display:flex; flex-direction:column; gap:12px; font-size:14px;'>");
            sb.Append(StatusRow("Arduino", status[3], status[3] == "online"));
            sb.Append(StatusRow("Conveyor 1", status[0], status[0] == "running"));
            sb.Append(StatusRow("Conveyor 2", status[1], status[1] == "running"));
            sb.Append(StatusRow("Box Position", status[2], true));
            sb.Append(string.Format(
                "<div style='text-align:right; font-size:11px; color:#aaa; margin-top:4px;'>" +
                "Last updated: {0}</div>", HtmlEncode(status[4])
            ));
            sb.Append("</div>");

            litMonitoring.Text = sb.ToString();
        }


        // ──────────────────────────────────────────────────────────────────────
        // HELPERS
        // ──────────────────────────────────────────────────────────────────────
        // Builds a styled alert HTML block.
        private string StatusAlert(string type, string message)
        {
            string bg = type == "success" ? "#e8f5e9" : "#ffebee";
            string border = type == "success" ? "#43a047" : "#e53935";
            string color = type == "success" ? "#2e7d32" : "#c62828";

            return string.Format(
                "<div style='margin-top:16px;padding:12px 16px;border-radius:6px;" +
                "background:{0};border-left:4px solid {1};color:{2};font-size:14px;'>{3}</div>",
                bg, border, color, message
            );
        }

        // for use in DisplayMachineStatus
        // builds one status row: "Label - value badge"
        private string StatusRow(string label, string value, bool isActive)
        {
            string badgeClass = isActive ? "badge-green" : "badge-red";
            string dot = isActive ? "🟢" : "🔴";

            if (label == "Box Position")
            {
                badgeClass = "badge-blue";
                dot = "📦";
            }

            return string.Format(
                "<div style='display:flex; justify-content:space-between; align-items:center;" +
                "padding:10px 14px; border-radius:6px; background:#f9f9f9; border:1px solid #eee;'>" +
                "<span style='font-weight:600; color:#555;'>{0}</span>" +
                "<div style='display:flex; align-items:center; gap:8px;'>" +
                "<span>{2}</span>" +
                "<span class='badge {1}'>{3}</span>" +
                "</div>" +
                "</div>",
                label,
                badgeClass,
                dot,
                HtmlEncode(value).ToUpper()
            );
        }

        // Escapes HTML special characters to prevent XSS.
        private string HtmlEncode(string input)
        {
            if (string.IsNullOrEmpty(input)) return "";
            return System.Web.HttpUtility.HtmlEncode(input);
        }
    }
}
