import express from "express";
import { getAdminToken, populateDummyStock } from "../controllers/admin.controller";
import verifyAdmin from "../middlewares/admin.middleware";

const router = express.Router();

router.post("/get-token", getAdminToken);
router.post("/populate-db/:id", verifyAdmin, populateDummyStock);

export default router;