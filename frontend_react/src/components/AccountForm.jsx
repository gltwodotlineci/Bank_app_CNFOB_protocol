import React, { useEffect, useState } from "react";

function AccountForm() {
  const [banks, setBanks] = useState([]);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    bank: "",
    number: "",
    amount: "",
    active: "true",
  });

  useEffect(() => {
    const loaded = window.BANKS || [];
    setBanks(loaded);
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      if (!formData.bank) {
        setMessage("Please select a bank");
        return;
      }

      const payload = {
        number: formData.number,
        amount: formData.amount,
        active: formData.active === "true",
      };

      const response = await fetch(
        `/api/banks/${formData.bank}/accounts/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          credentials: "same-origin",
          body: JSON.stringify(payload),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data?.detail || "Error creating account");
        return;
      }

      setMessage("Account created successfully");

      setFormData({
        bank: "",
        number: "",
        amount: "",
        active: "true",
      });
    } catch (err) {
      setMessage("Network error");
    }
  };

  function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(
            cookie.substring(name.length + 1)
          );
          break;
        }
      }
    }

    return cookieValue;
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-3xl mx-auto bg-white rounded-2xl shadow-2xl p-8 border border-gray-200 mt-10"
    >
      {message && (
        <div
          style={{
            marginBottom: "15px",
            color: message.includes("success") ? "green" : "red",
            fontWeight: "bold",
          }}
        >
          {message}
        </div>
      )}

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-2">
          Select Bank
        </label>

        <select
          name="bank"
          value={formData.bank}
          onChange={handleChange}
          className="w-full bg-white border border-gray-500 rounded-lg px-4 py-3 shadow-md"
        >
          <option value="">-- Choose a bank --</option>

          {banks.map((bank) => (
            <option key={bank.id} value={bank.id}>
              {bank.name}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-2">
          Account Number
        </label>

        <input
          type="text"
          name="number"
          maxLength="20"
          value={formData.number}
          onChange={handleChange}
          className="w-full border border-gray-500 rounded-lg px-4 py-3"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-2">
          Initial Balance
        </label>

        <input
          type="number"
          step="0.01"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          className="w-full border border-gray-500 rounded-lg px-4 py-3"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-2">
          Status
        </label>

        <select
          name="active"
          value={formData.active}
          onChange={handleChange}
          className="w-full border border-gray-500 rounded-lg px-4 py-3"
        >
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
      </div>

      <div className="flex justify-end pt-4">
        <button
          type="submit"
          className="px-8 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition"
        >
          Create Account
        </button>
      </div>
    </form>
  );
}

export default AccountForm;
