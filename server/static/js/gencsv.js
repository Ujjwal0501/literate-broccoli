var PREFIX = "CY";
const BASE = 36;
const MAX_PRODUCT_ID = 2176782336;

function validate(start, count) {
    const end = start + count;
    // ensure count and start are positive and within bounds
    if (isNaN(start) || isNaN(count) || !(start >= 0 && count > 0 && start < MAX_PRODUCT_ID && end <= MAX_PRODUCT_ID)) {
        throw new Error("Invalid start or count values");
    }
}

// Function to convert a number to the extended base-36 string
function convertNumberToBase36(number) {
    if (0 <= number < BASE**6) {
        const base36Chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let base36Str = '';
        for (let i = 0; i < 6; i++) {
            const [quotient, remainder] = [Math.floor(number / BASE), number % BASE];
            number = quotient;
            base36Str = base36Chars[remainder] + base36Str;
        }
        return PREFIX + base36Str;
    } else {
        throw new Error("Number must be between 0 and 36^6-1 for this conversion.");
    }
}

function generate_skus(start, count, prefix) {
    PREFIX = prefix
    validate(start, count);

    // Generate the list [start, end)
    const result = Array.from({ length: count }, (_, id) => convertNumberToBase36(start + id));
    console.table(result);
    return result.join('\n');
}
