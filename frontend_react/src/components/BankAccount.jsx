import React, { useEffect, useState } from "react";
import BankForm from "./BankForm.jsx";
import AccountForm from "./AccountForm.jsx";
import UpdateBank from "./UpdateBank.jsx";

function BankAccount() {
  const [activeForm, setActiveForm] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [banks, setBanks] = useState([]);
  const [selectedBank, setSelectedBank] = useState("");

  useEffect(() => {
    setBanks(window.BANKS || []);
  }, []);

  return (
    <div>
      {successMessage && (
        <div
          style={{
            color: "green",
            fontWeight: "bold",
            marginBottom: "10px",
          }}
        >
          {successMessage}
        </div>
      )}

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <button onClick={() => setActiveForm("bank")}>New Bank</button>

        <button onClick={() => setActiveForm("account")}>New Account</button>

        <button onClick={() => setActiveForm("update_bank")}>
          Update Bank
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        {activeForm === "bank" && (
          <BankForm setSuccessMessage={setSuccessMessage} />
        )}

        {activeForm === "account" && (
          <AccountForm setSuccessMessage={setSuccessMessage} />
        )}

        {activeForm === "update_bank" && (
          <div>
            <label>Select Bank</label>
            <br />

            <select
              value={selectedBank}
              onChange={(e) => setSelectedBank(e.target.value)}
              className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
            >
              <option value="">-- Choose a bank --</option>

              {banks.map((bank) => (
                <option key={bank.id} value={bank.id}>
                  {bank.name}
                </option>
              ))}
            </select>

            {selectedBank && (
              <div style={{ marginTop: "20px" }}>
                <UpdateBank
                  bankId={selectedBank}
                  setSuccessMessage={setSuccessMessage}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default BankAccount;
