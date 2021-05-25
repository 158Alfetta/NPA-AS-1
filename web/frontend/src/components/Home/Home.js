import "./home.css";
import "./home2.css";
import { useHistory } from "react-router-dom";

const Home = () => {

  let history = useHistory();

  return (
    <>
      <div className="App">

        <header className="masthead">
          <div className="container">
            <div className="intro-text">
              <div className="intro-heading text-uppercase">
                NettySight
              </div>
              <div className="intro-lead-in">Manage your configuration data at once</div>
              <div
                className="btn btn-primary btn-xl text-uppercase js-scroll-trigger"
                onClick={() => history.push("devices/")}
              >
                Launch App
              </div>
            </div>
          </div>
        </header>

        <section className="page-section" id="services">
          <div className="container">
            <div className="row">
              <div className="col-lg-12 text-center">
                <h2 className="section-heading text-uppercase">Services</h2>
                <h3 className="section-subheading text-muted">
                  We create a simply and manageable tools of your configuration data for the propose of migration.
                </h3>
              </div>
            </div>
            <div className="row text-center">
              <div className="col-md-4">
                <span className="fa-stack fa-4x">
                  <i className="fa fa-circle fa-stack-2x text-primary"></i>
                  <i className="fa fa-shopping-cart fa-stack-1x fa-inverse"></i>
                </span>
                <h4 className="service-heading">Decrease Error on Task</h4>
                <p className="text-muted">
                User error in the migration process, some configuration of the old system may be missing from open configuration data in .txt files.
                </p>
              </div>
              <div className="col-md-4">
                <span className="fa-stack fa-4x">
                  <i className="fa fa-circle fa-stack-2x text-primary"></i>
                  <i className="fa fa-laptop fa-stack-1x fa-inverse"></i>
                </span>
                <h4 className="service-heading">Mobile Device Accessible</h4>
                <p className="text-muted">
                  Everytime and everywhere on your devices, A text file of configuration is obviously hard to read on mobile devices.
                </p>
              </div>
              <div className="col-md-4">
                <span className="fa-stack fa-4x">
                  <i className="fa fa-circle fa-stack-2x text-primary"></i>
                  <i className="fa fa-lock fa-stack-1x fa-inverse"></i>
                </span>
                <h4 className="service-heading">Ready to Use Report</h4>
                <p className="text-muted">
                Provide a ready to use report for engineers, decrease time for preparation in migration processes.
                </p>
              </div>
            </div>
          </div>
        </section>

        <footer className="footer">
          <div className="container">
            <div className="row align-items-center">
              <div className="col-md-4">
                <span className="copyright">
                  NettySight @NPA-2020 Assignment
                </span>
              </div>
              <div className="col-md-4">
                <ul className="list-inline quicklinks">
                  <li className="list-inline-item">
                    <a href="#something">Privacy Policy</a>
                  </li>
                  <li className="list-inline-item">
                    <a href="#something">Terms of Use</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Home;
