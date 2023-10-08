import logo from "../../icons/logoxs.png"

function Header() {
    return (
        <nav class="navbar navbar-light bg-light p">
            <div class="container-fluid">
                <img src={logo} alt="" width="140" height="94" class="d-inline-block align-text-top py-2"/>
            </div>
        </nav>            
    );
  }

  export default Header;
