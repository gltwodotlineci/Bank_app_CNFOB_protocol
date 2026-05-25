const bankSelect = document.getElementById("bank-select");
const accountSelect = document.getElementById("account-select");
const operationsBody = document.getElementById("operations-body");

let allOperations = [];


async function loadBanks() {

    try {

        const response = await fetch("/api/banks/");
        const banks = await response.json();

        bankSelect.innerHTML = `
            <option value="">-- Select Bank --</option>
        `;

        banks.forEach(bank => {

            bankSelect.innerHTML += `
                <option value="${bank.id}">
                    ${bank.name}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);

        bankSelect.innerHTML = `
            <option value="">
                Error loading banks
            </option>
        `;
    }
}


async function loadAccounts(bankId) {

    accountSelect.innerHTML = `
        <option value="">Loading...</option>
    `;

    try {

        const response = await fetch(`/api/banks/${bankId}/accounts/`);
        const accounts = await response.json();

        accountSelect.innerHTML = `
            <option value="">All</option>
        `;

        accounts.forEach(account => {

            accountSelect.innerHTML += `
                <option value="${account.id}">
                    ${account.number}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);

        accountSelect.innerHTML = `
            <option value="">
                Error loading accounts
            </option>
        `;
    }
}


bankSelect.addEventListener("change", function () {

    const bankId = this.value;

    if (!bankId) {

        accountSelect.innerHTML = `
            <option value="">All</option>
        `;

        return;
    }

    loadAccounts(bankId);
});


document.addEventListener(
    "DOMContentLoaded",
    loadBanks
);


accountSelect.addEventListener("change", function () {

    const accountId = this.value;
    const bankId = bankSelect.value;

    if (!bankId || !accountId) {
        return;
    }

    loadOperations(bankId, accountId);
});


async function loadOperations(bankId, accountId) {

    operationsBody.innerHTML = `
        <tr>
            <td colspan="8" class="text-center">
                Loading...
            </td>
        </tr>
    `;

    try {

        const response = await fetch(
            `/api/banks/${bankId}/accounts/${accountId}/operations/`
        );

        const operations = await response.json();

        allOperations = operations;
        console.log("Allll Oooperations: ", operation => operation.pointed);

        renderOperations(allOperations);

    } catch (error) {

        console.error(error);

        operationsBody.innerHTML = `
            <tr>
                <td colspan="8"
                    class="text-center text-danger py-4">
                    Error loading operations
                </td>
            </tr>
        `;
    }
}


function renderOperations(operations) {

    operationsBody.innerHTML = "";

    if (!operations.length) {

        operationsBody.innerHTML = `
            <tr>
                <td colspan="8"
                    class="text-center text-muted py-4">
                    No operations found
                </td>
            </tr>
        `;

        return;
    }

    operations.forEach(operation => {

        operationsBody.innerHTML += `
            <tr>

                <td>${operation.date || ""}</td>

                <td>${operation.label || ""}</td>

                <td class="text-end text-success fw-bold">
                    ${operation.credit_or_debit === "C"
                        ? operation.amount
                        : ""}
                </td>

                <td class="text-end text-danger fw-bold">
                    ${operation.credit_or_debit === "D"
                        ? operation.amount
                        : ""}
                </td>

                <td class="text-end">
                    ${operation.credit_or_debit === "N"
                        ? operation.amount
                        : ""}
                </td>

                <td class="text-center">
                    <input
                        type="checkbox"
                        class="form-check-input"
                        ${operation.pointed ? "checked" : ""}
                    >
                </td>

                <td>
                    ${operation.pointed_date || ""}
                </td>

                <td>
                    ${operation.pointer_person || ""}
                </td>

            </tr>
        `;
    });
}

document
    .querySelectorAll("input[name='pointage']")
    .forEach(radio => {

        radio.addEventListener("change", function () {

            if (this.value === "all") {
                renderOperations(allOperations);
                return;
            }

            const filtered = allOperations.filter(operation => {

                const isPointed = operation.pointed === true;

                if (this.value === "pointed") {
                    return isPointed;
                }

                if (this.value === "non_pointed") {
                    return !isPointed;
                }

                return true;
            });

            renderOperations(filtered);
        });
    });
