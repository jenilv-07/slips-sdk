from fides.evaluation.ti_aggregation import AverageConfidenceTIAggregation
from fides.evaluation.ti_evaluation import MaxConfidenceTIEvaluation
from simulations.environment import generate_and_run
from simulations.model import SimulationConfiguration
from simulations.peer import PeerBehavior
from simulations.visualisation import plot_simulation_result

if __name__ == '__main__':
    simulation_configuration = SimulationConfiguration(
        benign_targets=1,
        malicious_targets=1,
        malicious_peers_lie_about_targets=1.0,
        peers_distribution={
            PeerBehavior.CONFIDENT_CORRECT: 2,
            PeerBehavior.UNCERTAIN_PEER: 1,
            PeerBehavior.CONFIDENT_INCORRECT: 0,
            PeerBehavior.MALICIOUS_PEER: 1,
        },
        simulation_length=200,
        malicious_peers_lie_since=25,
        service_history_size=100,
        pre_trusted_peers_count=0,
        initial_reputation=0.0,
        local_slips_acts_as=PeerBehavior.CONFIDENT_CORRECT,
        evaluation_strategy=MaxConfidenceTIEvaluation(),
        ti_aggregation_strategy=AverageConfidenceTIAggregation()
    )

    result = generate_and_run(simulation_configuration)
    plot_simulation_result(result, save_output='figure_6_1.png')
