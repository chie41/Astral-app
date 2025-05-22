-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2025 at 09:35 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aimodel`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `generate_random_string` (`len` INT) RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_general_ci DETERMINISTIC BEGIN
    DECLARE chars VARCHAR(62) DEFAULT 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    DECLARE output VARCHAR(255) DEFAULT '';
    DECLARE i INT DEFAULT 0;

    WHILE i < len DO
        SET output = CONCAT(output, SUBSTRING(chars, FLOOR(1 + RAND() * 62), 1));
        SET i = i + 1;
    END WHILE;

    RETURN output;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `chat_sesion`
--

CREATE TABLE `chat_sesion` (
  `sessionID` int(11) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `userID` varchar(8) DEFAULT NULL,
  `proID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_sesion`
--

INSERT INTO `chat_sesion` (`sessionID`, `subject`, `userID`, `proID`) VALUES
(1, 'Phân loại text', 'a2DrRUx9', 1000),
(2, 'Phân loại bài tập', 'a2DrRUx9', 1001),
(3, 'Phân loại bài tập trên lớp', 'a2DrRUx9', NULL),
(4, 'Phân loại sách giáo khoa', 'a2DrRUx9', NULL),
(5, 'Gợi ý dự án về động vật', 'Ls90Qu8l', 1002),
(6, 'Giá nhà ở Vin Group', 'Ls90Qu8l', 1003),
(7, 'Giá nhà ở SunHouse', 'Ls90Qu8l', NULL),
(8, 'Gạo', 'Ls90Qu8l', 1004),
(9, 'Tin tức trên báo', 'Ls90Qu8l', 1005),
(10, 'Từ mới Tiếng Anh', 'izf9cURZ', 1006),
(11, 'Ngữ pháp', 'izf9cURZ', 1007),
(12, 'Giá cổ phiếu trên sàn LVon', 'I0yjYPEm', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `messageId` int(11) NOT NULL,
  `sessionID` int(11) DEFAULT NULL,
  `sender` enum('chatbot','user') NOT NULL,
  `message` text DEFAULT NULL,
  `sendTime` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`messageId`, `sessionID`, `sender`, `message`, `sendTime`) VALUES
(1, 1, 'user', 'Hi, I want to create a machine learning model to predict future sales based on past transaction data. Can you help me?', '2025-05-21 02:34:02'),
(2, 1, 'chatbot', 'Create an AutoML Project: Predicting Sales Revenue\n1. Prepare Your Data\nMake sure your CSV file includes relevant columns, such as:\nProduct Name\nDate\nQuantity Sold\nRevenue (target column)\nAt least a few hundred rows are recommended for better results.\n2. Set Up the Project\nSteps to follow:\nUpload your dataset\nSelect target column: e.g., Revenue\nChoose task type: Regression\nOptional: Set forecast range (e.g., next 30 days)\n3. Train the Model\nThe system will automatically:\nClean and process your data\nTrain multiple models\nSelect the best-performing one\n4. Evaluate the Model  Once training is complete, you will be able to:\nView model performance metrics (e.g., RMSE, MAE, R²)\nCompare different models accuracy\nAnalyze feature importance to see which factors most influence revenue\nInspect predictions on validation/test data\n5. Make Predictions  After selecting the best model, you can:\nInput new data (e.g., upcoming product sales forecasts)\nGet predicted revenue outputs\nExport results as CSV or view them in charts/tables\n6. Deploy or Export the Model (optional)  For production use, you can:\nDeploy the model as an API for real-time predictions\nExport the trained model file (e.g., .pkl or .onnx) for integration into apps or services', '2025-05-21 02:34:02'),
(3, 2, 'user', 'Tôi muốn tạo model để phân loại thông tin bài tập dựa trên văn bản trên trang web abc.xyz.com', '2025-05-21 02:34:16'),
(4, 2, 'chatbot', 'Ok đây là phương pháp tôi đưa ra cho bạn .......Bạn thấy có hợp lí không?', '2025-05-21 02:34:16'),
(5, 2, 'user', 'Tôi thấy chỗ này hơi khó hiểu và không đúng ý tôi....... Bạn cần làm thế này....', '2025-05-21 02:34:16'),
(6, 2, 'chatbot', 'Vậy tôi đề xuất 1 phương pháp khác như sau:..... Bạn thấy thế nào?', '2025-05-21 02:34:16'),
(7, 5, 'user', 'Tôi cần 1 mô hình để phân loại sản phẩm dựa trên hình ảnh động vật', '2025-05-21 02:34:16'),
(8, 5, 'chatbot', 'Ok đây là phương pháp tôi đưa ra cho bạn .......Bạn thấy có hợp lí không?', '2025-05-21 02:34:16'),
(9, 6, 'user', 'Tôi cần 1 mô hình để phân loại giái nhà ở vin Group', '2025-05-21 02:34:16'),
(10, 6, 'chatbot', 'Ok đây là phương pháp tôi đưa ra cho bạn .......Bạn thấy có hợp lí không?', '2025-05-21 02:34:16'),
(11, 6, 'user', 'Tôi thấy chưa hợp lí. Bạn cần giải thích rõ hơn........', '2025-05-21 02:34:16'),
(12, 6, 'chatbot', 'Đây là phương án thay thế: ...... Bạn thấy thế nào', '2025-05-21 02:34:16'),
(13, 6, 'user', 'Chỗ này vẫn chưa rõ ràng.....', '2025-05-21 02:34:16'),
(14, 6, 'chatbot', 'À! Tôi hiểu rồi.Đây là phương án thay thế: ...... Bạn thấy thế nào', '2025-05-21 02:34:16'),
(15, 8, 'user', 'Bạn có thể giúp tôi tạo 1 dự án phân tích các loại gạo dựa trên hình ảnh giúp tôi không?', '2025-05-21 02:34:16'),
(16, 8, 'chatbot', 'Đây là phương án tôi đưa ra..... Bạn hãy cung cấp thêm thông tin để tôi phân tích chi tiết và rõ hơn.', '2025-05-21 02:34:16'),
(17, 9, 'user', 'Bạn có thể giúp tôi phân tích các tin tức dựa trên cá trang báo không', '2025-05-21 02:34:16'),
(18, 9, 'chatbot', 'Đây là 1 bản kế hoạch cụ thể hơn.......', '2025-05-21 02:34:16'),
(19, 10, 'user', 'Tôi cần tạo 1 mô hình phân tích từ vựng Tiếng Anh trên các bài báo', '2025-05-21 02:34:16'),
(20, 10, 'chatbot', 'Đây là phương pháp của tôi:.........', '2025-05-21 02:34:16'),
(21, 11, 'user', 'Bạn có thể giúp tôi tạo 1 mô hình phân tích ngữ pháp tiếng Anh qua các tài liệu được không', '2025-05-21 02:34:16'),
(22, 11, 'chatbot', 'Để tạo 1 mô hình phân tích, trước hết chúng ta cần.......', '2025-05-21 02:34:16'),
(23, 12, 'user', 'Bạn giúp tôi tạo mô hình phân tích gia scoor  phiếu trên sàn LVon nhé', '2025-05-21 02:34:16'),
(24, 12, 'chatbot', 'Để tạo 1 mô hình phân tích, trước hết chúng ta cần.......', '2025-05-21 02:34:16'),
(25, 12, 'user', 'Tôi thấy chưa hợp lí lắm.....', '2025-05-21 02:34:16'),
(26, 12, 'chatbot', 'Đây là phương pháp tôi đã chỉnh sửa lại........... Bạn cung cấp thông tin thêm cho tôi nhé.', '2025-05-21 02:34:16'),
(27, 7, 'user', 'Giúp tôi tạo 1 mô hình phân tích giá nhà Sun House nhé', '2025-05-21 02:34:16'),
(28, 7, 'chatbot', 'Để tạo 1 mô hình phân tích, trước hết chúng ta cần.......', '2025-05-21 02:34:16'),
(29, 7, 'user', 'tôi thấy có vấn đề ở chỗ này ......', '2025-05-21 02:34:16'),
(30, 7, 'chatbot', 'Đây là 1 phương pháp mới dựa trên các gợi ý từ bạn........', '2025-05-21 02:34:16'),
(31, 7, 'user', 'Tôi thấy vẫn còn chỗ chưa thích hợp', '2025-05-21 02:34:16'),
(32, 7, 'chatbot', 'Bạn nói hợp lí. Đây là phương pháp khác....... Có chỗ nào chưa hợp lí bạn xem xét nhé.', '2025-05-21 02:34:16'),
(33, 7, 'user', 'Tôi thấy vẫn sai sai. Chưa hợp ý tôi', '2025-05-21 02:34:16'),
(34, 7, 'chatbot', 'Ý tưởng của bạn nghe có vẻ hợp lí nhưng lại vẫn còn 1 số lỗi bạn chưa hiểu hết......', '2025-05-21 02:34:16'),
(35, 3, 'user', 'Giúp tôi tạo 1 mô hình phân tích bài tập trên lớp nhé', '2025-05-21 02:34:16'),
(36, 3, 'chatbot', 'Đây là phương pháp của tôi:.........', '2025-05-21 02:34:16'),
(37, 3, 'user', 'Bạn làm khá tốt mà chưa vừa ý tôi.......', '2025-05-21 02:34:16'),
(38, 3, 'chatbot', 'Ý tưởng của bạn khá phi thực tế..........', '2025-05-21 02:34:16'),
(39, 4, 'user', 'Bạn có thể giúp tôi tạo 1 mô hình phân tích bài tập nhé', '2025-05-21 02:34:16'),
(40, 4, 'chatbot', 'Trước tiên để phân tích để tạo mô hình chúng ta cần.......', '2025-05-21 02:34:16');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `proId` int(11) NOT NULL,
  `userID` varchar(8) DEFAULT NULL,
  `type` enum('image classification','text classification','tabular classification','multimodal classification') DEFAULT NULL,
  `description` text DEFAULT NULL,
  `proName` varchar(200) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`proId`, `userID`, `type`, `description`, `proName`, `date`) VALUES
(1000, 'a2DrRUx9', 'text classification', 'Phân loại thông tin sản phẩm dựa trên văn bản', 'Sản phẩm trên văn bản', '2024-11-23'),
(1001, 'a2DrRUx9', 'text classification', 'Phân loại thông tin bài tập dựa trên văn bản', 'Bài tập văn bản', '2024-10-01'),
(1002, 'Ls90Qu8l', 'image classification', 'Phân loại động vật dựa trên trang web được cung cấp', 'TRang web động vật', '2025-09-04'),
(1003, 'Ls90Qu8l', 'tabular classification', 'Phân loại giá nhà ở khu  bất động sản Vin Group', 'Giá nhà ở Vin Group', '2024-12-05'),
(1004, 'Ls90Qu8l', 'image classification', 'Phân loại gạo', 'Gạo', '2025-02-23'),
(1005, 'Ls90Qu8l', 'text classification', 'Phân loại tin tức dựa trên bài báo', 'Tin tức trên báo', '2025-09-05'),
(1006, 'izf9cURZ', 'text classification', 'Phân loại từ mới qua các bài báo tiếng Anh', 'Từ mới Tiếng Anh', '2023-05-06'),
(1007, 'izf9cURZ', 'text classification', 'Phân loại từ vựng Tiếng Anh', 'Từ vựng Tiếng Anh', '2024-10-28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userId` varchar(8) NOT NULL,
  `email` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `dateOfBirth` date DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userId`, `email`, `name`, `dateOfBirth`, `password`) VALUES
('a2DrRUx9', 'toentoen123@gmail.com', 'Toen Anderson', '1977-09-08', 'Toen@123'),
('I0yjYPEm', 'vutrumicraft@gmail.com', 'Nguyễn Trung Chung', '2000-01-31', 'TrChung@123'),
('izf9cURZ', 'kiwikiwi@gmail.com', 'KiWi Trần', '2000-11-02', 'IloveKiwi123'),
('Ls90Qu8l', 'chickenThomas65@gmail.com', 'Thomas Tom', '1999-02-16', 'ThomasandChicken@123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat_sesion`
--
ALTER TABLE `chat_sesion`
  ADD PRIMARY KEY (`sessionID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `proID` (`proID`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`messageId`),
  ADD KEY `sessionID` (`sessionID`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`proId`),
  ADD KEY `userID` (`userID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userId`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat_sesion`
--
ALTER TABLE `chat_sesion`
  MODIFY `sessionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `messageId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `proId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1008;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_sesion`
--
ALTER TABLE `chat_sesion`
  ADD CONSTRAINT `chat_sesion_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userId`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_sesion_ibfk_2` FOREIGN KEY (`proID`) REFERENCES `projects` (`proId`) ON DELETE SET NULL;

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`sessionID`) REFERENCES `chat_sesion` (`sessionID`) ON DELETE CASCADE;

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userId`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
