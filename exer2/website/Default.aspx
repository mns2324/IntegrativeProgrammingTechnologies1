<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="WebApplication8.WebForm1" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Student Record System</title>
    <style>
        /* ===== RESET & BASE ===== */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            color: #333;
            min-height: 100vh;

        }

        /* ===== TOP NAVIGATION BAR ===== */
        .navbar {
            background: #1a237e;
            color: white;
            padding: 0 30px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }

        .navbar .brand {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .navbar .brand span {
            color: #90caf9;
        }

        .navbar .nav-info {
            font-size: 13px;
            opacity: 0.8;
        }

        /* ===== PAGE WRAPPER ===== */
        .page-wrapper {
            max-width: 1440px;
            margin: 40px auto;
            padding: 0 20px;
        }

        /* ===== PAGE HEADER ===== */
        .page-header {
            margin-bottom: 30px;
        }

        .page-header h1 {
            font-size: 26px;
            color: #1a237e;
            font-weight: 700;
        }

        .page-header p {
            color: #666;
            font-size: 14px;
            margin-top: 4px;
        }

        /* ===== CARD ===== */
        .card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            overflow: hidden;
        }

        .card-header {
            background: #1a237e;
            color: white;
            padding: 16px 24px;
            font-size: 15px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-header .icon {
            font-size: 18px;
        }

        .card-body {
            padding: 28px 24px;
        }

        /* ===== FORM GRID ===== */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-group label {
            font-size: 13px;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group label .required {
            color: #e53935;
            margin-left: 2px;
        }

        /* Override ASP.NET TextBox to look like a styled input */
        .form-group input[type="text"] {
            width: 100%;
            padding: 10px 14px;
            border: 1.5px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            color: #333;
            transition: border-color 0.2s, box-shadow 0.2s;
            background: #fafafa;
        }

        .form-group input[type="text"]:focus {
            outline: none;
            border-color: #3949ab;
            box-shadow: 0 0 0 3px rgba(57,73,171,0.12);
            background: white;
        }

        /* ===== BUTTON ROW ===== */
        .btn-row {
            margin-top: 24px;
            display: flex;
            gap: 12px;
            align-items: center;
        }

        /* Override ASP.NET Button */
        .btn-primary {
            padding: 11px 28px;
            background: #1a237e;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            letter-spacing: 0.3px;
        }

        .btn-primary:hover {
            background: #283593;
            transform: translateY(-2px);
        }

        .btn-primary:active {
            transform: translateY(0);
        }

        .btn-reset {
            padding: 11px 20px;
            background: transparent;
            color: #666;
            border: 1.5px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: border-color 0.2s, color 0.2s;
        }

        .btn-reset:hover {
            border-color: #999;
            color: #333;
        }

        /* ===== ALERT / STATUS MESSAGE ===== */
        .alert {
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 14px;
            margin-top: 16px;
            display: none; /* shown via JS after postback */
        }

        .alert-success {
            background: #e8f5e9;
            border-left: 4px solid #43a047;
            color: #2e7d32;
        }

        /* ===== SECTION TITLE (above table card) ===== */
        .section-title {
            font-size: 18px;
            font-weight: 700;
            color: #1a237e;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ===== TABLE STYLES ===== */
        /*
            The table HTML is generated in Default.aspx.cs
            and injected into <asp:Literal ID="litTable">.
            These CSS classes are applied there.
        */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }

        .data-table thead th {
            background: #e8eaf6;
            color: #1a237e;
            padding: 12px 16px;
            text-align: left;
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #c5cae9;
        }

        .data-table tbody tr {
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.15s;
        }

        .data-table tbody tr:hover {
            background: #f5f7ff;
        }

        .data-table tbody td {
            padding: 12px 16px;
            color: #444;
            vertical-align: middle;
        }

        .data-table tbody tr:last-child {
            border-bottom: none;
        }

        /* ===== BADGE (for course and gender) ===== */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .badge-blue  { background: #e3f2fd; color: #1565c0; }
        .badge-pink  { background: #fce4ec; color: #880e4f; }
        .badge-green { background: #e8f5e9; color: #2e7d32; }

        /* ===== EMPTY STATE ===== */
        .empty-state {
            text-align: center;
            padding: 50px 20px;
            color: #aaa;
            font-size: 15px;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            color: #aaa;
            font-size: 12px;
            padding: 20px 0 40px;
        }

        /* ===== RESPONSIVENESS FOR SMALL SCREENS ===== */
        @media (max-width: 640px) {
            .form-grid { grid-template-columns: 1fr; }
            .navbar { padding: 0 16px; }
            .page-wrapper { margin: 20px auto; padding: 0 12px; }
        }

        .fourcontainersdiv {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .inventoryandlogsdiv {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .monitoringandordersdiv {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>

    <!-- Navigation Bar -->
    <div class="navbar">
        <div class="brand">&#127979; Smart Fruit <span>Inventory System</span></div>
        <div class="nav-info">Log Out</div>
    </div>

    <form id="form1" runat="server">
    <div class="page-wrapper">

        <!-- Page Header -->
        <div class="page-header">
            <h1>Admin Dashboard</h1>
            <p>Welcome back, admin!</p>
        </div>

        <div class="fourcontainersdiv">
            <div class="card">
                test
                <div class="card-body">Total Fruits</div>
            </div>
            <div class="card">
                test
                <div class="card-body">Total Orders</div>
            </div>
            <div class="card">
                test
                <div class="card-body">Pending Orders</div>
            </div>
            <div class="card">
                test
                <div class="card-body">Machine Status</div>
            </div>
        </div>

        <!-- ===== ADD STUDENT CARD ===== -->
        <div class="inventoryandlogsdiv">
            <div class="card">
                <div class="card-header">
                    <span class="icon">&#10010;</span>
                    Fruit Inventory
                </div>
                <div class="card-body">
                    <div class="form-grid">

                        <div class="form-group">
                            <label>Student ID <span class="required">*</span></label>
                            <asp:TextBox ID="txtid" runat="server" CssClass="txt-input" placeholder="e.g. 1001" />
                        </div>

                        <div class="form-group">
                            <label>Full Name <span class="required">*</span></label>
                            <asp:TextBox ID="txtname" runat="server" CssClass="txt-input" placeholder="e.g. Juan Dela Cruz" />
                        </div>

                        <div class="form-group">
                            <label>Course <span class="required">*</span></label>
                            <asp:TextBox ID="txtcourse" runat="server" CssClass="txt-input" placeholder="e.g. BSIT" />
                        </div>

                        <div class="form-group">
                            <label>Gender <span class="required">*</span></label>
                            <asp:TextBox ID="txtgender" runat="server" CssClass="txt-input" placeholder="Male / Female" />
                        </div>

                        <div class="form-group">
                            <label>Year Level <span class="required">*</span></label>
                            <asp:TextBox ID="txtyear" runat="server" CssClass="txt-input" placeholder="e.g. 1st Year" />
                        </div>

                    </div>

                    <div class="btn-row">
                        <asp:Button
                            ID="Button1"
                            runat="server"
                            Text="Save Record"
                            CssClass="btn-primary"
                            OnClick="Button1_Click" />
                        <button type="reset" class="btn-reset">Clear</button>
                    </div>

                    <!-- Status message rendered from code-behind -->
                    <asp:Literal ID="litStatus" runat="server" />
                </div>
            </div>
            <div class="card">
                <div class="card-header">Recent Sorting Logs</div>
                <div class="card-body"></div>
            </div>
        </div>

        <div class="monitoringandordersdiv">
            <div class="card">
                <div class="card-header">Machine Monitoring</div>
                <div class="card-body"></div>
            </div>

            <!-- ===== STUDENT LIST CARD ===== -->
            <div class="card">
                <div class="card-header">
                    Pending Orders
                    <span style="margin-left:auto; font-size:12px; opacity:0.8;">
                        Data via Java DLL (IKVM)
                    </span>
                </div>
                <div class="card-body" style="padding:0;">
                    <!-- litTable is populated in code-behind with a styled HTML table -->
                    <asp:Literal ID="litTable" runat="server" />
                </div>
            </div>

            <div class="footer">
                Smart Fruit Sorting System (Admin Webpage) &bull; ASP.NET + Java (IKVM) + MySQL
            </div>
        </div>


    </div>
    </form>

</body>
</html>
