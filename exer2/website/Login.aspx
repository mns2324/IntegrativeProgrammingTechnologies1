<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Login.aspx.cs" Inherits="SmartFruitInventorySystem.Login" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <title>Smart Fruit Inventory System /// Login</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .navbar {
            background: #1a237e;
            color: white;
            padding: 0 30px;
            height: 60px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .navbar .brand { font-size: 20px; font-weight: 700; letter-spacing: 1px; }
        .navbar .brand span { color: #90caf9; }
        .login-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            width: 380px;
            overflow: hidden;
        }
        .login-header {
            background: #1a237e;
            color: white;
            padding: 20px 28px;
            font-size: 15px;
            font-weight: 600;
        }
        .login-body { padding: 28px; }
        .form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px; }
        .form-group label {
            font-size: 12px; font-weight: 600; color: #555;
            text-transform: uppercase; letter-spacing: 0.5px;
        }
        .form-group input[type="text"],
        .form-group input[type="password"] {
            width: 100%; padding: 10px 14px;
            border: 1.5px solid #ddd; border-radius: 6px;
            font-size: 14px; color: #333; background: #fafafa;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-group input:focus {
            outline: none; border-color: #3949ab;
            box-shadow: 0 0 0 3px rgba(57,73,171,0.12);
            background: white;
        }
        .btn-login {
            width: 100%; padding: 11px;
            background: #1a237e; color: white;
            border: none; border-radius: 6px;
            font-size: 14px; font-weight: 600;
            cursor: pointer; transition: background 0.2s;
        }
        .btn-login:hover { background: #283593; }
        .alert-error {
            margin-top: 14px; padding: 10px 14px;
            background: #ffebee; border-left: 4px solid #e53935;
            color: #c62828; font-size: 13px; border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="brand">Smart Fruit <span>Inventory System</span></div>
    </div>
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-header">&#128274; Administrator Login</div>
            <div class="login-body">
                <form id="Form1" runat="server">
                    <div class="form-group">
                        <label>Username</label>
                        <asp:TextBox ID="txtUser" runat="server" CssClass="form-control" />
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <asp:TextBox ID="txtPass" runat="server" TextMode="Password" />
                    </div>
                    <asp:Button ID="BtnLogin" runat="server" Text="Login"
                                CssClass="btn-login" OnClick="BtnLogin_Click" />
                    <asp:Literal ID="litError" runat="server" />
                </form>
            </div>
        </div>
    </div>
</body>
</html>