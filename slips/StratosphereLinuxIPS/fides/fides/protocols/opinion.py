from typing import Dict

from fides.evaluation.ti_aggregation import TIAggregation, PeerReport
from fides.messaging.model import PeerIntelligenceResponse
from fides.model.alert import Alert
from fides.model.aliases import PeerId, Target
from fides.model.configuration import TrustModelConfiguration
from fides.model.peer_trust_data import PeerTrustData, TrustMatrix
from fides.model.threat_intelligence import SlipsThreatIntelligence
from fides.persistence.threat_intelligence import ThreatIntelligenceDatabase


class OpinionAggregator:
    """
    Class responsible for evaluation of the intelligence received from the network.
    """

    def __init__(self,
                 configuration: TrustModelConfiguration,
                 ti_db: ThreatIntelligenceDatabase,
                 ti_aggregation: TIAggregation):
        self.__configuration = configuration
        self.__ti_db = ti_db
        self.__ti_aggregation = ti_aggregation

    def evaluate_alert(self, peer_trust: PeerTrustData, alert: Alert) -> SlipsThreatIntelligence:
        """Evaluates given data about alert and produces aggregated intelligence for Slips."""

        alert_trust = max(self.__configuration.alert_trust_from_unknown, peer_trust.service_trust)
        score = alert.score
        confidence = alert.confidence * alert_trust
        return SlipsThreatIntelligence(score=score, confidence=confidence, target=alert.target)

    def evaluate_intelligence_response(self,
                                       target: Target,
                                       data: Dict[PeerId, PeerIntelligenceResponse],
                                       trust_matrix: TrustMatrix) -> SlipsThreatIntelligence:
        """Evaluates given threat intelligence report from the network."""
        reports = [PeerReport(report_ti=ti.intelligence,
                              reporter_trust=trust_matrix[peer_id]
                              ) for peer_id, ti in data.items()]
        ti = self.__ti_aggregation.assemble_peer_opinion(data=reports)
        return SlipsThreatIntelligence(score=ti.score, confidence=ti.confidence, target=target)
