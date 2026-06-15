document.addEventListener("DOMContentLoaded", function () {

    const dropdownBtn = document.getElementById("banksDropdownBtn");
    const dropdownMenu = document.getElementById("banksDropdownMenu");
    const arrow = document.getElementById("dropdownArrow");

    const btnBank = document.getElementById("btnBank");
    const btnAccount = document.getElementById("btnAccount");

    const bankContainer = document.getElementById("bankFormContainer");
    const accountForm = document.getElementById("accountForm");

    let loaded = false;

    function hideAll() {

        if (bankContainer) {
            bankContainer.classList.add("hidden");
        }

        if (accountForm) {
            accountForm.classList.add("hidden");
        }
    }

    function showBankContainer() {

        hideAll();

        if (bankContainer) {
            bankContainer.classList.remove("hidden");
        }
    }

    function showAccountForm() {

        hideAll();

        if (accountForm) {
            accountForm.classList.remove("hidden");
        }
    }

    // ==========================
    // NEW BANK
    // ==========================

    if (btnBank) {

        btnBank.addEventListener("click", async function () {

            try {

                const response = await fetch("/bank_form/");

                bankContainer.innerHTML = await response.text();

                showBankContainer();

            } catch (error) {

                console.error(error);
            }
        });
    }

    // ==========================
    // NEW ACCOUNT
    // ==========================

    if (btnAccount) {

        btnAccount.addEventListener("click", function () {

            showAccountForm();
        });
    }

    // ==========================
    // BANKS DROPDOWN
    // ==========================

    if (dropdownBtn && dropdownMenu) {

        dropdownBtn.addEventListener("click", async () => {

            dropdownMenu.classList.toggle("hidden");

            if (arrow) {

                arrow.textContent =
                    dropdownMenu.classList.contains("hidden")
                        ? "▼"
                        : "▲";
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

                    item.type = "button";

                    item.className =
                        "block w-full text-left px-4 py-3 hover:bg-gray-100 transition";

                    item.textContent =
                        bank.bank_name || bank.name || "Unnamed Bank";

                    item.addEventListener("click", async () => {

                        try {

                            const response = await fetch(
                                `/update_bank_form/${bank.id}/`
                            );

                            bankContainer.innerHTML =
                                await response.text();

                            showBankContainer();

                            dropdownMenu.classList.add("hidden");

                            if (arrow) {
                                arrow.textContent = "▼";
                            }

                        } catch (error) {

                            console.error(error);
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
    }

});
