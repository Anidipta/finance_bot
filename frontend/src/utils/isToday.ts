const isToday = (dateString: string): boolean => {
    const givenDate = new Date(dateString);
    const today = new Date();

    return (
        givenDate.getDate() === today.getDate() &&
        givenDate.getMonth() === today.getMonth() &&
        givenDate.getFullYear() === today.getFullYear()
    );
};

export default isToday;