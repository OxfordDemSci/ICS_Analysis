
export function GenerateReport(
        api_uri,
        name,
        threshold,
        topic,
        postcode_area,
        beneficiary,
        uoa,
        funder) {

    return new Promise((resolve, reject) => {
        
        let uoa_prm = (uoa === "All") ? null : uoa;
        let uri = api_uri + "download_pdf?threshold=" + threshold + "&topic=" + topic + "&postcode_area=" + postcode_area + "&beneficiary=" + beneficiary + "&uoa=" + uoa_prm + "&funder=" + funder;
        var link = document.createElement("a");
        link.setAttribute('download', name);
        link.href = uri;
        document.body.appendChild(link);
        link.click();
        link.remove();

        resolve(link);
    });
}