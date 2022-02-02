

const usdFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    useGrouping: true,
    // maximumSignificantDigits: 2,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

const usdShortFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    useGrouping: true,
    // maximumSignificantDigits: 6,
    notation: "compact",
    compactDisplay: "short",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

const numberFormatter = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

const numberShortFormatter = new Intl.NumberFormat('en-US', {
    notation: "compact",
    compactDisplay: "short",
    // maximumSignificantDigits: 6,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});
