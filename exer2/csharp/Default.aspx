<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="WebApplication1._Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
            Enter ID
            <asp:TextBox ID="txtid" runat="server"></asp:TextBox>
            <br /><br />
            Enter Name
            <asp:TextBox ID="txtname" runat="server"></asp:TextBox>
            <br /><br />
            Enter Course
            <asp:TextBox ID="txtcourse" runat="server"></asp:TextBox>
            <br /><br />
            Enter Gender
            <asp:TextBox ID="txtgender" runat="server"></asp:TextBox>
            <br /><br />
            Enter Year
            <asp:TextBox ID="txtyear" runat="server"></asp:TextBox>
            <br /><br />
    <asp:Button ID="Button1" runat="server" Text="Click Me" OnClick="Button1_Click" />
    <asp:Literal ID="litTable" runat="server"></asp:Literal>
    </div>
    </form>
</body>
</html>
