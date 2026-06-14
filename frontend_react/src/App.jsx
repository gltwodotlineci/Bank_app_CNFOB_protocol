import Operations from "./components/Operations.jsx";
import BankAccount from "./components/BankAccount.jsx";

function App() {
  const page = window.REACT_PAGE;

  if (page === "operations") {
    return <Operations />;
  }

  if (page === "bank") {
    return <BankAccount />;
  }

  return <div>Unknown page: {String(page)}</div>;
}

export default App;
