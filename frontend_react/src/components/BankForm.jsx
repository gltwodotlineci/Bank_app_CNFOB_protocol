import React, { useEffect, useState } from "react";

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

function BankForm({ setSuccessMessage }) {
  const [companies, setCompanies] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    code: "",
    branch_code: "",
    swift: "",
    rib_key: "",
    holder_name: "",
    adresse: "",
    phone: "",
    email: "",
    zip_code: "",
    country_key: "",
    company: "",
  });

  useEffect(() => {
    const loaded = window.COMPANIES || [];
    setCompanies(loaded);
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccessMessage("");

    try {
      const response = await fetch("/api/banks/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        credentials: "same-origin",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("API error:", data);
        setSuccessMessage("Error creating bank");
        return;
      }

      setSuccessMessage(data.message);

      setFormData({
        name: "",
        code: "",
        branch_code: "",
        swift: "",
        rib_key: "",
        holder_name: "",
        adresse: "",
        phone: "",
        email: "",
        zip_code: "",
        country_key: "",
        company: "",
      });
    } catch (err) {
      console.error("Network error:", err);
      setSuccessMessage("Network error");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-semibold mb-2">
          Bank Name
        </label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <input
          type="text"
          name="code"
          placeholder="Bank Code"
          value={formData.code}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <input
          type="text"
          name="branch_code"
          placeholder="Branch Code"
          value={formData.branch_code}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <input
          type="text"
          name="swift"
          placeholder="SWIFT / BIC"
          value={formData.swift}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <input
          type="text"
          name="rib_key"
          placeholder="RIB Key"
          value={formData.rib_key}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />
      </div>

      <input
        type="text"
        name="holder_name"
        placeholder="Account Holder"
        value={formData.holder_name}
        onChange={handleChange}
        className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
      />

      <input
        type="text"
        name="adresse"
        placeholder="Bank Address"
        value={formData.adresse}
        onChange={handleChange}
        className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="text"
          name="phone"
          placeholder="Phone"
          value={formData.phone}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          type="text"
          name="zip_code"
          placeholder="ZIP Code"
          value={formData.zip_code}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <input
          type="text"
          name="country_key"
          placeholder="Country Key"
          value={formData.country_key}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        />

        <select
          name="company"
          value={formData.company}
          onChange={handleChange}
          className="w-full bg-gray-50 border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm"
        >
          <option value="">Select company</option>

          {companies.map((company) => (
            <option key={company.id} value={company.id}>
              {company.name}
            </option>
          ))}
        </select>
      </div>

      <div className="pt-6 flex justify-end">
        <button
          type="submit"
          className="px-8 py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition"
        >
          Validate
        </button>
      </div>
    </form>
  );
}

export default BankForm;
