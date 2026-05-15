document.addEventListener("DOMContentLoaded", function () {

    const btnBank = document.getElementById("btnBank");
    const btnAccount = document.getElementById("btnAccount");

    const bankForm = document.getElementById("bankForm");
    const accountForm = document.getElementById("accountForm");

    function hideAll() {
        if (bankForm) bankForm.classList.add("hidden");
        if (accountForm) accountForm.classList.add("hidden");
    }

    function openBankForm() {
        hideAll();
        if (bankForm) bankForm.classList.remove("hidden");
    }

    function openAccountForm() {
        hideAll();
        if (accountForm) accountForm.classList.remove("hidden");
    }

    if (btnBank) {
        btnBank.addEventListener("click", openBankForm);
    }

    if (btnAccount) {
        btnAccount.addEventListener("click", openAccountForm);
    }

    window.openBankForm = openBankForm;
    window.openAccountForm = openAccountForm;
});


// dorp down

document.addEventListener("DOMContentLoaded", function () {

    const dropdownBtn = document.getElementById("banksDropdownBtn");
    const dropdownMenu = document.getElementById("banksDropdownMenu");
    const arrow = document.getElementById("dropdownArrow");

    let loaded = false;

    if (!dropdownBtn || !dropdownMenu) return;

    dropdownBtn.addEventListener("click", async () => {

        dropdownMenu.classList.toggle("hidden");

        if (arrow) {
            arrow.textContent = dropdownMenu.classList.contains("hidden") ? "▼" : "▲";
        }

        if (loaded) return;

        try {

            const response = await fetch("/api/banks/");
            const banks = await response.json();

            dropdownMenu.innerHTML = "";

            if (!banks.length) {
                dropdownMenu.innerHTML = `
                    <div class="px-4 py-3 text-gray-500">
                        No banks found
                    </div>
                `;
                return;
            }

            banks.forEach(bank => {

                const item = document.createElement("button");

                item.className =
                    "block w-full text-left px-4 py-3 hover:bg-gray-100 transition";

                item.textContent = bank.bank_name || bank.name || "Unnamed Bank";

                item.addEventListener("click", () => {

                    console.log("Selected bank:", bank);

                    fillBankForm(bank);

                    dropdownMenu.classList.add("hidden");
                    if (arrow) arrow.textContent = "▼";

                    if (window.openBankForm) {
                        window.openBankForm();
                    }

                });

                dropdownMenu.appendChild(item);
            });

            loaded = true;

        } catch (error) {

            console.error(error);

            dropdownMenu.innerHTML = `
                <div class="px-4 py-3 text-red-500">
                    Error loading banks
                </div>
            `;
        }

    });
});


// Filling Form

function fillBankForm(bank) {

    const set = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.value = value || "";
    };

    set("name", bank?.bank_name || bank?.name);
    set("bank_code", bank?.bank_code || bank?.code);
    set("bic", bank?.bic);
    set("rib", bank?.rib);
    set("branch_code", bank?.branch_code);
    set("account_holder", bank?.holder_name);
    set("address", bank?.adresse);
    set("email", bank?.email);
    set("phone", bank?.phone);
    set("zip_code", bank?.zip_code);

}
