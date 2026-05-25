function setupIBANListeners() {

    const countryKey = document.getElementById("conuntry_key2");
    const bankCode = document.getElementById("code_b");
    const branchCode = document.getElementById("brch_code");
    const accountNb = document.getElementById("account_nb");
    const ribKey = document.getElementById("key_rib");
    const ibanField = document.getElementById("iban");

    if (!countryKey || !bankCode || !branchCode || !accountNb || !ribKey || !ibanField) {
        return;
    }

    const updateIBAN = () => {

        const iban = "FR" +
            countryKey.value +
            ribKey.value +
            bankCode.value +
            branchCode.value +
            accountNb.value;

        ibanField.value = iban.replace(/\s/g, "").replace(/(.{4})/g, "$1 ").trim();
    };

    accountNb.removeEventListener("input", updateIBAN);
    accountNb.addEventListener("input", updateIBAN);

    updateIBAN();
}

document.addEventListener("DOMContentLoaded", setupIBANListeners);

document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.target.id === "bank-details") {
        setupIBANListeners();
    }
});


document.querySelector("select[name='bank']").addEventListener("change", function () {
    window.selectedBankId = this.value;
});


document.getElementById("create-btn").addEventListener("click", function () {

    if (!window.selectedBankId) {
        alert("Please select a bank first");
        return;
    }

    createAccount(window.selectedBankId);
});


async function createAccount(bankId) {

    const accountNb = document.getElementById("account_nb");
    const amount = document.getElementById("amount");
    const active = document.getElementById("active");
    const toast = document.getElementById("toast2");

    if (!accountNb || !amount || !active) return;

    const data = {
        number: accountNb.value,
        amount: amount.value,
        active: active.value === "true",
        bank_id: bankId
    };

    try {
        console.log("The bank id is:___ ", bankId);
        const res = await fetch(`/api/banks/${bankId}/accounts/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        toast.innerHTML = `
            <div class="bg-green-100 text-green-800 px-4 py-2 rounded-lg">
                Account created successfully
            </div>
        `;

        console.log(result);

    } catch (error) {

        toast.innerHTML = `
            <div class="bg-red-100 text-red-800 px-4 py-2 rounded-lg">
                Error creating account
            </div>
        `;

        console.error(error);
    }
}


function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
}
