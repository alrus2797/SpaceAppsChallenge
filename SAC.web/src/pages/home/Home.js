import Header from '../../components/header/Header';
import SearchBar from '../../components/searchbar/SearchBar';
import Title from '../../components/title/Title';
import PlanningButton from '../../components/planningbtn/PlanningButton';
import './home.css';

function Home() {
    return (
      <div className="App">
        <div>
          <Header/>
        </div>
        <div>
          <div class="pt-5 pb-2">
            <Title/>
          </div>
          <div class="search-bar-container py-5">
            <SearchBar/>
          </div>
          <PlanningButton/>
        </div>
      </div>
    );
  }

export default Home;
