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

function UpdateBank({ bankId, setSuccessMessage }) {
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
    setCompanies(window.COMPANIES || []);
  }, []);

  useEffect(() => {
    if (!bankId) return;

    const loadBank = async () => {
      try {
        const response = await fetch(`/api/banks/${bankId}/`);

        if (!response.ok) return;

        const data = await response.json();

        setFormData({
          name: data.name || "",
          code: data.code || "",
          branch_code: data.branch_code || "",
          swift: data.swift || "",
          rib_key: data.rib_key || "",
          holder_name: data.holder_name || "",
          adresse: data.adresse || "",
          phone: data.phone || "",
          email: data.email || "",
          zip_code: data.zip_code || "",
          country_key: data.country_key || "",
          company: data.company || "",
        });
      } catch (err) {
        console.error(err);
      }
    };

    loadBank();
  }, [bankId]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSuccessMessage("");

    const payload = {
      holder_name: formData.holder_name,
      phone: formData.phone,
      adresse: formData.adresse,
      email: formData.email,
    };

    try {
      const response = await fetch(`/api/banks/${bankId}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setSuccessMessage("Error updating bank");
        return;
      }

      setSuccessMessage(data.message || "Bank updated successfully");
    } catch (err) {
      console.error(err);
      setSuccessMessage("Network error");
    }
  };

  const readonlyStyle =
    "w-full bg-gray-100 border-2 border-gray-300 rounded-lg px-4 py-3 shadow-sm text-gray-500";

  const editableStyle =
    "w-full bg-white border-2 border-gray-400 rounded-lg px-4 py-3 shadow-sm";

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-semibold mb-2">
          Bank Name
        </label>
        <input
          type="text"
          value={formData.name}
          disabled
          className={readonlyStyle}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <input value={formData.code} disabled className={readonlyStyle} />
        <input value={formData.branch_code} disabled className={readonlyStyle} />
        <input value={formData.swift} disabled className={readonlyStyle} />
        <input value={formData.rib_key} disabled className={readonlyStyle} />
      </div>

      <input value={formData.zip_code} disabled className={readonlyStyle} />

      <input value={formData.country_key} disabled className={readonlyStyle} />

      <input
        type="text"
        name="holder_name"
        placeholder="Account Holder"
        value={formData.holder_name}
        onChange={handleChange}
        className={editableStyle}
      />

      <input
        type="text"
        name="adresse"
        placeholder="Address"
        value={formData.adresse}
        onChange={handleChange}
        className={editableStyle}
      />

      <input
        type="text"
        name="phone"
        placeholder="Phone"
        value={formData.phone}
        onChange={handleChange}
        className={editableStyle}
      />

      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        className={editableStyle}
      />

      <div className="pt-6 flex justify-end">
        <button
          type="submit"
          className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition"
        >
          Update Bank
        </button>
      </div>
    </form>
  );
}

export default UpdateBank;
