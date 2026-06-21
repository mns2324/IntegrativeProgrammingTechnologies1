<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Dashboard.aspx.cs" Inherits="SmartFruitInventorySystem.Dashboard" %>

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

        /* ===== BADGE (for arduino status) ===== */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .badge-blue  { background: #e3f2fd; color: #1565c0; }
        .badge-green { background: #e8f5e9; color: #2e7d32; }
        .badge-red { background: #ffebee; color: #c62828; }

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

        /* ===== STAT CARDS (fourcontainersdiv) ===== */
        .fourcontainersdiv {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .fourcontainersdiv .card {
            display: flex; /* make icon display next to text */
            flex-direction: row;
            align-items: center;
            gap: 16px;
            padding: 12px;
        }

        .fourcontainersdiv .card-body {
            padding: 0; /* no padding for table */
        }

        .card-icon {
            width: 100px;
            height: 100px;
            border-radius: 8px;
            flex-shrink: 0; /* prevents image from squishing */
        }

        .card-value {
            font-size: 22px;
            font-weight: 700;
            color: #1a237e;
        }

        .card-label {
            font-size: 14px;
            margin-bottom: 2px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        .inventoryandlogsdiv {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .inventoryandlogsdiv .card-body {
            padding: 0; /* no padding for table */
        }

        .logs-scroll {
            max-height: 350px;
            overflow-y: auto;
        }

        /* keep the header fixed while scrolling */
        .logs-scroll .data-table thead th {
            position: sticky;
            top: 0;
            z-index: 1;
        }

        .monitoringandordersdiv {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .fruit-img {
            width:50px;
            height:50px;
            object-fit:cover;
            border-radius:6px;
        }
        /* ===== EDIT / DELETE BUTTONS for fruit table ===== */
        .edit-btn,
        .delete-btn {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 6px 14px;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
            letter-spacing: 0.3px;
        }

        .edit-btn {
            background: #e8eaf6;
            color: #1a237e;
        }

        .edit-btn:hover {
            background: #1a237e;
            color: white;
            box-shadow: 0 2px 8px rgba(26, 35, 126, 0.25);
            transform: translateY(-1px);
        }

        .delete-btn {
            background: #ffebee;
            color: #c62828;
        }

        .delete-btn:hover {
            background: #c62828;
            color: white;
            box-shadow: 0 2px 8px rgba(198, 40, 40, 0.25);
            transform: translateY(-1px);
        }
        .logout-btn {
            background:transparent; 
            border:1px solid rgba(255,255,255,0.5); 
            color:white;
            padding: 6px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.8);
            color: #1a237e;
            box-shadow: 0 2px 8px rgba(26, 35, 126, 0.75);
            transform: translateY(-1px);
        }
        .edit-btn:active,
        .delete-btn:active
        .logout-btn:active {
            transform: translateY(0);
            box-shadow: none;
        }

    </style>
</head>
<body>
    <form id="form1" runat="server">
        <!-- Navigation Bar -->
        <div class="navbar">
            <div class="brand">🍅 Smart Fruit <span>Inventory System</span></div>
            <div class="nav-info">
                <asp:Button ID="BtnLogout" class="logout-btn" runat="server" Text="Log Out" OnClick="BtnLogout_Click" />
            </div>
        </div>
                
        <%-- Hidden fields: carry JS values back to the server on postback --%>
        <asp:HiddenField ID="hfEditId"       runat="server" />
        <asp:HiddenField ID="hfEditName"     runat="server" />
        <asp:HiddenField ID="hfEditCategory" runat="server" />
        <asp:HiddenField ID="hfEditPrice"    runat="server" />
        <asp:HiddenField ID="hfEditQty"      runat="server" />
        <asp:HiddenField ID="hfEditImage"    runat="server" />
        <asp:HiddenField ID="hfDeleteId"     runat="server" />

        <%-- These buttons are invisible; JS clicks them to trigger postbacks --%>
        <asp:Button ID="BtnEdit" runat="server" style="display:none" OnClick="BtnEdit_Click" />
        <asp:Button ID="BtnDelete" runat="server" style="display:none" OnClick="BtnDelete_Click" />

        <div class="page-wrapper">
            <%-- Status message shown after postback --%>
            <asp:Literal ID="litStatus" runat="server" />
            <br />

            <!-- Page Header -->
            <div class="page-header">
                <h1>Admin Dashboard</h1>
                <p>Welcome back, admin!</p>
            </div>

            <div class="fourcontainersdiv">
                <div class="card">
                    <img src="https://placehold.co/100x100" alt="icon" class="card-icon" />
                    <div class="card-body">
                        <div class="card-label">Total Fruits</div>
                        <asp:Literal ID="litTotalFruits" runat="server" />            
                    </div>
                </div>
                <div class="card">
                    <img src="https://placehold.co/100x100" alt="icon" class="card-icon" />
                    <div class="card-body">
                        <div class="card-label">Total Orders</div>
                        <div id="totalOrders" class="card-value" style="color:deepskyblue">placeholder</div>
                    
                    </div>
                </div>
                <div class="card">
                    <img src="https://placehold.co/100x100" alt="icon" class="card-icon" />
                    <div class="card-body">
                        <div class="card-label">Pending Orders</div>
                        <div id="totalPendingOrders" class="card-value" style="color:darkorange">placeholder</div>
                    
                    </div>
                </div>
                <div class="card">
                    <img src="https://placehold.co/100x100" alt="icon" class="card-icon" />
                    <div class="card-body">
                        <div class="card-label">Machine Status</div>
                        <asp:Literal ID="litMachineStatus" runat="server" />                        
                    </div>
                </div>
            </div>

            <div class="inventoryandlogsdiv">
                <div class="card">
                    <div class="card-header">
                        Fruit Inventory
                    </div>
                    <div class="card-body">
                        <!-- this table is populated in code-behind with a styled HTML table -->
                        <asp:Literal ID="litFruitsTable" runat="server" />
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Recent Sorting Logs</div>
                    <div class="card-body">
                        <!-- this table is populated in code-behind with a styled HTML table -->
                        <div class="logs-scroll">
                            <asp:Literal ID="litLogsTable" runat="server" />
                        </div>
                    </div>
                </div>
            </div>

            <div class="monitoringandordersdiv">
                <div class="card">
                    <div class="card-header">Machine Monitoring</div>
                    <div class="card-body">
                        <asp:Literal ID="litMonitoring" runat="server" />
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        Pending Orders
                        <span style="margin-left:auto; font-size:12px; opacity:0.8;">
                            Data via Java DLL (IKVM)
                        </span>
                    </div>
                    <div class="card-body">
                        Placeholder
                    </div>
                </div>
            </div>

            <div class="footer">
                Smart Fruit Sorting System (Admin Webpage) &bull; ASP.NET (C#) + Java (IKVM) + Python + Arduino (C++) + MySQL 
            </div>
        </div>
    </form>
    <!-- ===== EDIT MODAL ===== -->
    <!-- pop-up modal for edit button, does clientside validation before submitting -->
    <div id="editModal" style="display:none; position:fixed; inset:0;background:rgba(0,0,0,0.60); z-index:1000; align-items:center; justify-content:center;">
        <div style="background:#fff; border-radius:10px; width:420px; max-width:95%;box-shadow:0 8px 32px rgba(0,0,0,0.2); padding:28px 28px 24px;">
            <h3 style="margin-bottom:20px; color:#1a237e; font-size:17px;">
                &#9998; Edit Fruit <span id="modalFruitId" style="color:#888; font-weight:400;"></span>
            </h3>

            <div style="display:flex; flex-direction:column; gap:14px;">
                <div>
                    <label style="font-size:12px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.5px;">
                        Fruit Name <span style="color:#e53935">*</span>
                    </label>
                    <input id="inpName" type="text"style="width:100%;margin-top:5px;padding:9px 12px;border:1.5px solid #ddd;border-radius:6px;font-size:14px;" />
                    <span id="errName" style="color:#c62828;font-size:12px;display:none;">
                        Fruit name is required.
                    </span>
                </div>
                <div>
                    <label style="font-size:12px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.5px;">
                        Category <span style="color:#e53935">*</span>
                    </label>
                    <input id="inpCategory" type="text"style="width:100%;margin-top:5px;padding:9px 12px;border:1.5px solid #ddd;border-radius:6px;font-size:14px;" />
                    <span id="errCategory" style="color:#c62828;font-size:12px;display:none;">
                        Category is required.
                    </span>
                </div>
                <div>
                    <label style="font-size:12px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.5px;">
                        Price <span style="color:#e53935">*</span>
                    </label>
                    <input id="inpPrice" type="number" min="0" step="0.01"style="width:100%;margin-top:5px;padding:9px 12px;border:1.5px solid #ddd;border-radius:6px;font-size:14px;" />
                    <span id="errPrice" style="color:#c62828;font-size:12px;display:none;">
                        Price must be a valid non-negative number.
                    </span>
                </div>
                <div>
                    <label style="font-size:12px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.5px;">
                        Quantity <span style="color:#e53935">*</span>
                    </label>
                    <input id="inpQty" type="number" min="0" step="1"style="width:100%;margin-top:5px;padding:9px 12px;border:1.5px solid #ddd;border-radius:6px;font-size:14px;" />
                    <span id="errQty" style="color:#c62828;font-size:12px;display:none;">
                        Quantity must be a whole non-negative number.
                    </span>
                </div>
                <div>
                    <label style="font-size:12px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.5px;">
                        Image Path
                    </label>
                    <input id="inpImage" type="text"style="width:100%;margin-top:5px;padding:9px 12px;border:1.5px solid #ddd;border-radius:6px;font-size:14px;" />
                </div>
            </div>

            <div style="margin-top:22px; display:flex; gap:10px; justify-content:flex-end;">
                <button onclick="closeEditModal()"style="padding:9px 20px;border:1.5px solid #ddd;background:transparent;border-radius:6px;cursor:pointer;font-size:14px;color:#555;">
                    Cancel
                </button>
                <button onclick="submitEdit()"style="padding:9px 24px;background:#1a237e;color:white;border:none;border-radius:6px;font-size:14px;font-weight:600;cursor:pointer;">
                    Save Changes
                </button>
            </div>
        </div>
    </div>
</body>
<script>
    var currentEditId = '';
    var mouseDownTarget = null;

    // ── EDIT ─────────────────────────────────────────────────────────────────
    function editFruit(id, name, category, price, qty, image) {
        currentEditId = id;
        document.getElementById('modalFruitId').textContent = '(ID: ' + id + ')';
        document.getElementById('inpName').value = name;
        document.getElementById('inpCategory').value = category;
        document.getElementById('inpPrice').value = price;
        document.getElementById('inpQty').value = qty;
        document.getElementById('inpImage').value = image;

        // Clear any previous validation errors if the user clicks edit again 
        // after triggering a validation error and exiting out of the modal.
        ['errName', 'errCategory', 'errPrice', 'errQty'].forEach(function (id) {
            document.getElementById(id).style.display = 'none';
        });
        ['inpName', 'inpCategory', 'inpPrice', 'inpQty'].forEach(function (id) {
            document.getElementById(id).style.borderColor = '#ddd';
        });

        document.getElementById('editModal').style.display = 'flex';
    }

    function closeEditModal() {
        document.getElementById('editModal').style.display = 'none';
    }
   
    document.getElementById('editModal').addEventListener('mousedown', function (e) {
        mouseDownTarget = e.target; // record where the click started
    });

    // editModal div is styled to make the entire page dark and overlays its child divs on top
    // the dark part is the editModal div which triggers this eventListener when you click on it
    document.getElementById('editModal').addEventListener('click', function (e) {
        // only close if BOTH the press and release were on the overlay itself
        if (e.target === this && mouseDownTarget === this) closeEditModal();
        mouseDownTarget = null;
    });

    // read all input values from the modal fields
    function submitEdit() {
        var name = document.getElementById('inpName').value.trim();
        var category = document.getElementById('inpCategory').value.trim();
        var price = document.getElementById('inpPrice').value.trim();
        var qty = document.getElementById('inpQty').value.trim();
        var image = document.getElementById('inpImage').value.trim();

        // ── Client-side validation ────────────────────────────────────────────
        var valid = true;

        function setErr(inputId, errId, show) {
            document.getElementById(inputId).style.borderColor = show ? '#e53935' : '#ddd';
            document.getElementById(errId).style.display = show ? 'inline' : 'none';
            if (show) valid = false;
        }

        setErr('inpName', 'errName', name === '');
        setErr('inpCategory', 'errCategory', category === '');
        setErr('inpPrice', 'errPrice', price === '' || isNaN(parseFloat(price)) || parseFloat(price) < 0);
        setErr('inpQty', 'errQty', qty === '' || !Number.isInteger(Number(qty)) || parseInt(qty) < 0);

        if (!valid) return;

        // Pass values to hidden fields then click the invisible BtnEdit btn to trigger the BtnEdit_Click function
        document.getElementById('<%= hfEditId.ClientID %>').value = currentEditId;
        document.getElementById('<%= hfEditName.ClientID %>').value = name;
        document.getElementById('<%= hfEditCategory.ClientID %>').value = category;
        document.getElementById('<%= hfEditPrice.ClientID %>').value = price;
        document.getElementById('<%= hfEditQty.ClientID %>').value = qty;
        document.getElementById('<%= hfEditImage.ClientID %>').value = image;
        document.getElementById('<%= BtnEdit.ClientID %>').click();
    }

    // ── DELETE ─────────────────────────────────────────────────────────────────
    function deleteFruit(id) {
        if (!confirm('Are you sure you want to delete Fruit #' + id + '? This cannot be undone.'))
            return;

        // put the fruit id into the hidden hfDeleteId field then click the invisible BtnDelete btn to trigger the BtnDelete_Click function
        document.getElementById('<%= hfDeleteId.ClientID %>').value = id;
        document.getElementById('<%= BtnDelete.ClientID %>').click();
    }
</script>
</html>
