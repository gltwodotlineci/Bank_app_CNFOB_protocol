import React, { useEffect, useMemo, useState } from "react";

function Operations() {

    const [banks, setBanks] = useState([]);
    const [accounts, setAccounts] = useState([]);
    const [operations, setOperations] = useState([]);

    const [selectedBank, setSelectedBank] = useState("");
    const [selectedAccount, setSelectedAccount] = useState("");

    const [filter, setFilter] = useState("all");

    const [usersMap, setUsersMap] = useState({});

    /* =========================
       LOAD BANKS
    ========================= */
    useEffect(() => {
        loadBanks();
    }, []);

    async function loadBanks() {

        try {

            const response = await fetch("/api/banks/");
            const data = await response.json();

            setBanks(data);

        } catch (error) {
            console.error(error);
        }
    }

    /* =========================
       LOAD ACCOUNTS
    ========================= */
    async function loadAccounts(bankId) {

        try {

            const response = await fetch(
                `/api/banks/${bankId}/accounts/`
            );

            const data = await response.json();

            setAccounts(data);

        } catch (error) {
            console.error(error);
        }
    }

    /* =========================
       LOAD OPERATIONS
    ========================= */
    async function loadOperations(bankId, accountId) {

        try {

            const response = await fetch(
                `/api/banks/${bankId}/accounts/${accountId}/operations/`
            );

            const data = await response.json();

            setOperations(data);

            loadUsers(data);

        } catch (error) {
            console.error(error);
        }
    }

    /* =========================
       LOAD USERS
    ========================= */
    async function loadUsers(operationsData) {

        const uniqueUsers = [
            ...new Set(
                operationsData
                    .map(op => op.pointer)
                    .filter(Boolean)
            )
        ];

        const newUsersMap = {};

        for (const userId of uniqueUsers) {

            try {

                const response = await fetch(`/api/users/${userId}/`);

                const user = await response.json();

                newUsersMap[userId] = user.username;

            } catch (error) {

                console.error(error);

                newUsersMap[userId] = userId;
            }
        }

        setUsersMap(newUsersMap);
    }

    /* =========================
       FORMAT DATE
    ========================= */
    function formatDate(dateString) {

        if (!dateString) return "";

        const date = new Date(dateString);

        return date.toLocaleDateString();
    }

    /* =========================
       BANK CHANGE
    ========================= */
    async function handleBankChange(event) {

        const bankId = event.target.value;

        setSelectedBank(bankId);
        setSelectedAccount("");

        setAccounts([]);
        setOperations([]);

        if (!bankId) return;

        loadAccounts(bankId);
    }

    /* =========================
       ACCOUNT CHANGE
    ========================= */
    async function handleAccountChange(event) {

        const accountId = event.target.value;

        setSelectedAccount(accountId);

        if (!selectedBank || !accountId) return;

        loadOperations(selectedBank, accountId);
    }

    /* =========================
       FILTERED OPERATIONS
    ========================= */
    const filteredOperations = useMemo(() => {

        if (filter === "all") {
            return operations;
        }

        if (filter === "pointed") {
            return operations.filter(op => op.pointed === true);
        }

        if (filter === "non_pointed") {
            return operations.filter(op => op.pointed === false);
        }

        return operations;

    }, [operations, filter]);

    /* =========================
       PATCH POINTING
    ========================= */
    async function togglePointing(operationId, checked) {

        try {

            const response = await fetch(
                `/api/banks/${selectedBank}/accounts/${selectedAccount}/operations/${operationId}/`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        pointed: checked
                    })
                }
            );

            const updated = await response.json();

            if (updated.pointer && !usersMap[updated.pointer]) {

                try {

                    const userResponse = await fetch(
                        `/api/users/${updated.pointer}/`
                    );

                    const userData = await userResponse.json();

                    setUsersMap(prev => ({
                        ...prev,
                        [updated.pointer]: userData.username
                    }));

                } catch (error) {
                    console.error(error);
                }
            }

            setOperations(prev =>
                prev.map(op =>
                    op.id === operationId
                        ? {
                            ...op,
                            pointed: updated.pointed,
                            date_pointed: updated.date_pointed,
                            pointer: updated.pointer
                        }
                        : op
                )
            );

        } catch (error) {
            console.error(error);
        }
    }

    /* =========================
       TOTALS
    ========================= */
    const totalCredit = filteredOperations
        .filter(op => op.credit_or_debit === "C")
        .reduce(
            (sum, op) => sum + parseFloat(op.amount || 0),
            0
        );

    const totalDebit = filteredOperations
        .filter(op => op.credit_or_debit === "D")
        .reduce(
            (sum, op) => sum + parseFloat(op.amount || 0),
            0
        );

    const totalSold = filteredOperations
        .filter(op => op.credit_or_debit === "N")
        .reduce(
            (sum, op) => sum + parseFloat(op.amount || 0),
            0
        );

    return (

        <div className="container-fluid mt-4">

            {/* FILTERS */}
            <div className="card shadow-sm mb-4">

                <div className="card-body">

                    <div className="row g-3 align-items-end">

                        {/* BANK */}
                        <div className="col-md-2">

                            <label className="form-label fw-bold">
                                Bank
                            </label>

                            <select
                                className="form-select"
                                value={selectedBank}
                                onChange={handleBankChange}
                            >

                                <option value="">
                                    -- Select Bank --
                                </option>

                                {banks.map(bank => (

                                    <option
                                        key={bank.id}
                                        value={bank.id}
                                    >
                                        {bank.name}
                                    </option>

                                ))}

                            </select>

                        </div>

                        {/* ACCOUNT */}
                        <div className="col-md-2">

                            <label className="form-label fw-bold">
                                Account N°
                            </label>

                            <select
                                className="form-select"
                                value={selectedAccount}
                                onChange={handleAccountChange}
                            >

                                <option value="">
                                    All
                                </option>

                                {accounts.map(account => (

                                    <option
                                        key={account.id}
                                        value={account.id}
                                    >
                                        {account.number}
                                    </option>

                                ))}

                            </select>

                        </div>

                        {/* FILTER */}
                        <div className="col-md-3">

                            <label className="form-label fw-bold d-block">
                                Pointage
                            </label>

                            <div className="d-flex gap-3">

                                <div className="form-check">

                                    <input
                                        className="form-check-input"
                                        type="radio"
                                        checked={filter === "pointed"}
                                        onChange={() => setFilter("pointed")}
                                    />

                                    <label className="form-check-label">
                                        Pointed
                                    </label>

                                </div>

                                <div className="form-check">

                                    <input
                                        className="form-check-input"
                                        type="radio"
                                        checked={filter === "non_pointed"}
                                        onChange={() => setFilter("non_pointed")}
                                    />

                                    <label className="form-check-label">
                                        Non Pointed
                                    </label>

                                </div>

                                <div className="form-check">

                                    <input
                                        className="form-check-input"
                                        type="radio"
                                        checked={filter === "all"}
                                        onChange={() => setFilter("all")}
                                    />

                                    <label className="form-check-label">
                                        All
                                    </label>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

            {/* TABLE */}
            <div className="card shadow-sm">

                <div className="card-body table-responsive">

                    <table className="table table-bordered table-hover align-middle">

                        <thead className="table-dark">

                            <tr>
                                <th>Date</th>
                                <th>Operation Label</th>
                                <th className="text-end">Credit</th>
                                <th className="text-end">Debit</th>
                                <th className="text-end">Sold</th>
                                <th className="text-center">Pointage</th>
                                <th>Pointed Date</th>
                                <th>Pointer Person</th>
                            </tr>

                        </thead>

                        <tbody>

                            {!filteredOperations.length && (

                                <tr>

                                    <td
                                        colSpan="8"
                                        className="text-center text-muted py-4"
                                    >
                                        No operations found
                                    </td>

                                </tr>
                            )}

                            {filteredOperations.map(operation => (

                                <tr key={operation.id}>

                                    <td>
                                        {formatDate(operation.date)}
                                    </td>

                                    <td>
                                        {operation.label}
                                    </td>

                                    <td className="text-end text-success fw-bold">

                                        {operation.credit_or_debit === "C"
                                            ? operation.amount
                                            : ""}

                                    </td>

                                    <td className="text-end text-danger fw-bold">

                                        {operation.credit_or_debit === "D"
                                            ? operation.amount
                                            : ""}

                                    </td>

                                    <td className="text-end">

                                        {operation.credit_or_debit === "N"
                                            ? operation.amount
                                            : ""}

                                    </td>

                                    <td className="text-center">

                                        <input
                                            type="checkbox"
                                            className="form-check-input"
                                            checked={operation.pointed}
                                            onChange={(e) =>
                                                togglePointing(
                                                    operation.id,
                                                    e.target.checked
                                                )
                                            }
                                        />

                                    </td>

                                    <td>
                                        {formatDate(
                                            operation.date_pointed
                                        )}
                                    </td>

                                    <td>
                                        {usersMap[operation.pointer] || ""}
                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>

            {/* TOTALS */}
            <div className="card shadow-sm mt-4">

                <div className="card-body">

                    <div className="row g-3 justify-content-end">

                        <div className="col-md-2">

                            <label className="form-label fw-bold">
                                Total Credit
                            </label>

                            <input
                                readOnly
                                className="form-control bg-light"
                                value={totalCredit.toFixed(2)}
                            />

                        </div>

                        <div className="col-md-2">

                            <label className="form-label fw-bold">
                                Total Debit
                            </label>

                            <input
                                readOnly
                                className="form-control bg-light"
                                value={totalDebit.toFixed(2)}
                            />

                        </div>

                        <div className="col-md-2">

                            <label className="form-label fw-bold">
                                Total Sold
                            </label>

                            <input
                                readOnly
                                className="form-control bg-light fw-bold"
                                value={totalSold.toFixed(2)}
                            />

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}

function getCookie(name) {

    const match = document.cookie.match(
        new RegExp("(^| )" + name + "=([^;]+)")
    );

    return match
        ? decodeURIComponent(match[2])
        : null;
}

export default Operations;
